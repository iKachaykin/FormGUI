import psycopg2
from Project.Question import Question


# Класс, реализующий уровень логики
class LogicTier:

    # Конструктор
    def __init__(self, localhost):
        self.localhost = localhost
        self.conn = None
        self.cur = None

    # Установка соединения с БД
    def connect(self):
        self.conn = psycopg2.connect(self.localhost)
        self.cur = self.conn.cursor()

    # Отключение от БД
    def disconnect(self):
        self.conn.close()
        self.cur.close()
        self.conn, self.cur = None, None

    # Коммит сделанных изменений
    def commit(self):
        return self.conn.commit()

    # Вспомогательный метод, создающий запрос
    def createQuery(self, table, columns=(), condition=None, order_by_expression=None):
        query = "SELECT "
        if len(columns) > 0:
            for column in columns:
                query += "\"%s\".\"%s\", " % (table, column)
            query = query[:len(query) - 2]
        else:
            query += "*"
        query += " FROM \"%s\"" % table
        if condition is not None:
            query += " WHERE %s" % condition
        if order_by_expression is not None:
            query += " ORDER BY \"%s\"" % order_by_expression
        return query

    # Метод, возвращающий все данные по запросу
    def getAllDataFromTable(self, table, *columns, **kwargs):
        condition, order_by_expression = kwargs.get('condition'), kwargs.get('order_by_expression')
        self.connect()
        self.cur.execute(self.createQuery(table, columns, condition, order_by_expression))
        data = self.cur.fetchall()
        self.disconnect()
        return data

    # Выбор одного из столбцов из результата select-запроса
    def selectColumnFromQuery(self, query_result, column):
        func_res = []
        for row in query_result:
            func_res.append(row[column])
        return func_res

    def getQuestions(self):
        questions = []
        self.connect()
        self.cur.execute(self.createQuery(
            'questions',
            columns=('question_id', 'question_text', 'question_tip', 'answer_type'),
            order_by_expression='question_id'))
        data = self.cur.fetchall()
        self.disconnect()
        for i in range(len(data)):
            row = data[i]
            questions.append(Question(row[0], row[1], row[2], row[3]))
            if row[3] == 'discrete':
                answers = self.getAllDataFromTable(
                    'answers_discrete', 'answer_text', 'answer_value', condition='question_id=%d' % row[0])
                questions[-1].set_answers(answers)
            elif row[3] == 'range':
                query_res = self.getAllDataFromTable(
                    'answers_range', 'lower_bound', 'upper_bound', condition='question_id=%s' % row[0]
                )
                questions[-1].set_bounds(query_res[0][0], query_res[0][1])
        return questions.copy()

    def getTransport(self):
        transport = []
        self.connect()
        self.cur.execute(self.createQuery(
            'transport_types',
            columns=('type_id', 'type_name', 'type_description'),
            order_by_expression='type_id'))
        transport = self.cur.fetchall()
        self.disconnect()
        return transport.copy()

    def getWeights(self, rows, cols):
        weights = [[0 for j in range(cols)] for i in range(rows)]
        self.connect()
        self.cur.execute(self.createQuery(
            'weights',
            columns=('question_id', 'type_id', 'weight_value')))
        data = self.cur.fetchall()
        self.disconnect()
        for d in data:
            weights[d[0]-1][d[1]-1] = d[2]
        return weights.copy()

    def setWeightsAndTransport(self, weights, transport):
        self.connect()
        self.cur.execute("DELETE FROM weights")
        self.cur.execute("DELETE FROM transport_types")
        for t in transport:
            self.cur.execute("INSERT INTO transport_types VALUES (%d, '%s', '%s')" % (t[0], t[1], t[2]))
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                self.cur.execute("INSERT INTO weights VALUES (%f, %d, %d)" % (weights[i][j], i+1, j+1))
        self.conn.commit()
        self.disconnect()

    def setWeightsAndQuestions(self, weights, questions):
        self.connect()
        self.cur.execute("DELETE FROM weights")
        self.cur.execute("DELETE FROM answers_discrete")
        self.cur.execute("DELETE FROM answers_range")
        self.cur.execute("DELETE FROM questions")
        for q in questions:
            self.cur.execute("INSERT INTO questions VALUES (%d, '%s', '%s', '%s')" % (q.id, q.text, q.tip, q.type))
            if q.type == 'discrete':
                for k, v in zip(q.answers.keys(), q.answers.values()):
                    self.cur.execute("INSERT INTO answers_discrete VALUES (%d, %f, '%s')" % (q.id, v, k))
            elif q.type == 'range':
                self.cur.execute("INSERT INTO answers_range VALUES (%d, %d, %d)" % (q.id, q.lower_bound, q.upper_bound))
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                self.cur.execute("INSERT INTO weights VALUES (%f, %d, %d)" % (weights[i][j], i+1, j+1))
        self.conn.commit()
        self.disconnect()
