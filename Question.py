class Question:

    def __init__(self, id, text,  tip, type):
        self.id = id
        self.text = text
        self.tip = tip
        self.type = type
        if type == 'discrete':
            self.answers = {}
        elif type == 'range':
            self.lower_bound, self.upper_bound = 0, 0

    def set_answers(self, answers):
        if self.type != 'discrete':
            raise ValueError('Type must be "discrete"!')
        for a in answers:
            self.answers[a[0]] = a[1]

    def set_bounds(self, lower_bound, upper_bound):
        if self.type != 'range':
            raise ValueError('Type must be "range"!')
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __str__(self):
        return '({0}, {1}, {2}, {3})'.format(self.id, self.text, self.tip, self.type)

    def __copy__(self):
        copy_ = Question(self.id, self.text, self.tip, self.type)
        if copy_.type == 'range':
            copy_.lower_bound = self.lower_bound
            copy_.upper_bound = self.upper_bound
        else:
            copy_.set_answers([(k, v) for k, v in zip(self.answers.keys(), self.answers.values())])
        return copy_

    def copy(self):
        return self.__copy__()
