from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip, QTableWidget, QTableWidgetItem, QTextEdit, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt
from Project.Question import Question


class ExpertQuestionsEditButtonWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)
        self.application = application
        self.index = index
        width_multiplier, height_multiplier = 0.5, 0.75
        self_width, self_height = QDesktopWidget().availableGeometry().width() * width_multiplier, \
                                  QDesktopWidget().availableGeometry().height() * height_multiplier
        self.resize(self_width, self_height)
        self.setFixedSize(self_width, self_height)
        self.moveToCenter()
        self.leftMargin, self.rightMargin, self.topMargin, self.bottomMargin, self.betweenMargin = \
            self_width * 0.02, self_width * 0.02, self_height * 0.05, self_height * 0.02, self_height * 0.05

        self.currentQuestion = 1
        self.question = Question(0, '', '', 'range')
        self.currentCol = -1
        self.transport = []
        self.weights = []

        self.titleText = 'Редактирование вопроса #%s'
        self.title = QLabel(self)
        self.title.setText(self.titleText % (self.currentQuestion+1))
        self.title.resize(self.title.sizeHint())
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

        self.questionTextEditLabelText = 'Текст вопроса'
        self.questionTextEditLabel = QLabel(self)
        self.questionTextEditLabel.setText(self.questionTextEditLabelText)
        self.questionTextEditLabel.resize(self.questionTextEditLabel.sizeHint())
        self.questionTextEditLabelX, self.questionTextEditLabelY = \
            self.leftMargin, self.titleY + self.title.height() + self.betweenMargin
        self.questionTextEditLabel.move(self.questionTextEditLabelX, self.questionTextEditLabelY)

        self.questionTextEdit = QTextEdit(self)
        self.questionTextEditX, self.questionTextEditY = \
            self.leftMargin, self.questionTextEditLabelY + self.questionTextEditLabel.height()
        self.questionTextEditWidth, self.questionTextEditHeight = \
            1.0 * (self.width() - self.leftMargin - self.rightMargin),\
            0.2 * (self.height() - self.topMargin - self.bottomMargin)
        self.questionTextEdit.move(self.questionTextEditX, self.questionTextEditY)
        self.questionTextEdit.resize(self.questionTextEditWidth, self.questionTextEditHeight)

        self.questionTipEditLabelText = 'Подсказка к вопросу'
        self.questionTipEditLabel = QLabel(self)
        self.questionTipEditLabel.setText(self.questionTipEditLabelText)
        self.questionTipEditLabel.resize(self.questionTipEditLabel.sizeHint())
        self.questionTipEditLabelX, self.questionTipEditLabelY = \
            self.leftMargin, self.questionTextEditY + self.questionTextEdit.height() + self.betweenMargin
        self.questionTipEditLabel.move(self.questionTextEditLabelX, self.questionTipEditLabelY)

        self.questionTipEdit = QTextEdit(self)
        self.questionTipEditX, self.questionTipEditY = \
            self.leftMargin, self.questionTipEditLabelY + self.questionTipEditLabel.height()
        self.questionTipEditWidth, self.questionTipEditHeight = \
            self.questionTextEditWidth, self.questionTextEditHeight
        self.questionTipEdit.move(self.questionTipEditX, self.questionTipEditY)
        self.questionTipEdit.resize(self.questionTipEditWidth, self.questionTipEditHeight)

        self.questionTypeComboBoxLabelText = 'Тип ответа'
        self.questionTypeComboBoxLabel = QLabel(self)
        self.questionTypeComboBoxLabel.setText(self.questionTypeComboBoxLabelText)
        self.questionTypeComboBoxLabel.resize(self.questionTypeComboBoxLabel.sizeHint())
        self.questionTypeComboBoxLabelX, self.questionTypeComboBoxLabelY = \
            self.leftMargin, self.questionTipEditY + self.questionTipEdit.height() + self.betweenMargin
        self.questionTypeComboBoxLabel.move(self.questionTypeComboBoxLabelX, self.questionTypeComboBoxLabelY)

        self.questionTypeComboBox = QComboBox(self)
        self.questionTypeComboBoxX, self.questionTypeComboBoxY = \
            self.leftMargin, self.questionTypeComboBoxLabelY + self.questionTypeComboBoxLabel.height()
        self.questionTypeComboBox.move(self.questionTypeComboBoxX, self.questionTypeComboBoxY)
        self.questionTypeComboBox.addItems(['Шкала', 'Набор'])
        self.questionTypeComboBox.resize(
            (self.width() - self.leftMargin - self.rightMargin - 2 * self.betweenMargin) / 3,
            self.questionTypeComboBox.height())
        self.questionTypeComboBox.setCurrentIndex(0)
        self.questionTypeComboBox.currentIndexChanged.connect(self.questionTypeComboBox_currentIndexChanged)

        self.rangeLeftBoundLabelText = 'Минимальное значение шкалы'
        self.rangeLeftBoundLabel = QLabel(self)
        self.rangeLeftBoundLabel.setText(self.rangeLeftBoundLabelText)
        self.rangeLeftBoundLabel.resize(self.rangeLeftBoundLabel.sizeHint())
        self.rangeLeftBoundLabelX, self.rangeLeftBoundLabelY = \
            self.questionTypeComboBoxX + self.questionTypeComboBox.width() + self.betweenMargin,\
            self.questionTypeComboBoxLabelY
        self.rangeLeftBoundLabel.move(self.rangeLeftBoundLabelX, self.rangeLeftBoundLabelY)

        self.rangeLeftBoundLineEdit = QLineEdit(self)
        self.rangeLeftBoundLineEdit.resize(self.questionTypeComboBox.size())
        self.rangeLeftBoundLineEdit.move(self.rangeLeftBoundLabelX,
                                         self.rangeLeftBoundLabelY + self.rangeLeftBoundLabel.height())

        self.rangeRightBoundLabelText = 'Максимальное значение шкалы'
        self.rangeRightBoundLabel = QLabel(self)
        self.rangeRightBoundLabel.setText(self.rangeRightBoundLabelText)
        self.rangeRightBoundLabel.resize(self.rangeRightBoundLabel.sizeHint())
        self.rangeRightBoundLabelX, self.rangeRightBoundLabelY = \
            self.rangeLeftBoundLineEdit.x() + self.rangeLeftBoundLineEdit.width() + self.betweenMargin,\
            self.rangeLeftBoundLabel.y()
        self.rangeRightBoundLabel.move(self.rangeRightBoundLabelX, self.rangeRightBoundLabelY)

        self.rangeRightBoundLineEdit = QLineEdit(self)
        self.rangeRightBoundLineEdit.resize(self.questionTypeComboBox.size())
        self.rangeRightBoundLineEdit.move(self.rangeRightBoundLabelX,
                                          self.rangeRightBoundLabelY + self.rangeRightBoundLabel.height())

        self.discreteLabelText = 'Набор возможных значений'
        self.discreteLabel = QLabel(self)
        self.discreteLabel.setText(self.discreteLabelText)
        self.discreteLabel.resize(self.discreteLabel.sizeHint())
        self.discreteLabelX, self.discreteLabelY = \
            self.questionTypeComboBoxX + self.questionTypeComboBox.width() + self.betweenMargin,\
            self.questionTypeComboBoxLabelY
        self.discreteLabel.move(self.discreteLabelX, self.discreteLabelY)
        self.discreteLabel.hide()

        self.discreteTable = QTableWidget(self)
        self.discreteTable.setRowCount(2)
        self.discreteTable.setVerticalHeaderItem(0, QTableWidgetItem('Слово'))
        self.discreteTable.setVerticalHeaderItem(1, QTableWidgetItem('Число'))
        self.discreteTable.horizontalHeader().hide()
        self.discreteTable.resize(0.4 * self.width(), 2 * self.questionTypeComboBox.height())
        self.discreteTable.move(self.discreteLabelX, self.discreteLabelY + self.discreteLabel.height())
        self.discreteTable.currentCellChanged.connect(self.discreteTable_currentCellChanged)
        self.discreteTable.hide()
        
        self.addButtonText = 'Добавить'
        self.addButton = QPushButton(self)
        self.addButton.setText(self.addButtonText)
        self.addButtonX, self.addButtonY = \
            self.discreteTable.x() + self.discreteTable.width() + self.betweenMargin, self.discreteLabel.y()
        self.addButtonWidth, self.addButtonHeight = \
            self.width() - self.leftMargin - 2 * self.betweenMargin - self.rightMargin - self.discreteTable.width() - \
            self.questionTypeComboBox.width(), \
            self.addButton.sizeHint().height()
        self.addButton.move(self.addButtonX, self.addButtonY)
        self.addButton.resize(self.addButtonWidth, self.addButtonHeight)
        self.addButton.clicked.connect(self.addButton_clicked)
        self.addButton.hide()

        self.deleteButtonText = 'Удалить'
        self.deleteButton = QPushButton(self)
        self.deleteButton.setText(self.deleteButtonText)
        self.deleteButtonX, self.deleteButtonY = \
            self.addButtonX, self.addButtonY + self.addButtonHeight + 0.0 * self.betweenMargin
        self.deleteButtonWidth, self.deleteButtonHeight = self.addButtonWidth, self.addButtonHeight
        self.deleteButton.move(self.deleteButtonX, self.deleteButtonY)
        self.deleteButton.resize(self.deleteButtonWidth, self.deleteButtonHeight)
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteButton_clicked)
        self.deleteButton.hide()

        self.clearButtonText = 'Очистить'
        self.clearButton = QPushButton(self)
        self.clearButton.setText(self.clearButtonText)
        self.clearButtonX, self.clearButtonY = \
            self.deleteButtonX, self.deleteButtonY + self.deleteButtonHeight + 0.0 * self.betweenMargin
        self.clearButtonWidth, self.clearButtonHeight = self.deleteButtonWidth, self.deleteButtonHeight
        self.clearButton.move(self.clearButtonX, self.clearButtonY)
        self.clearButton.resize(self.clearButtonWidth, self.clearButtonHeight)
        self.clearButton.clicked.connect(self.clearButton_clicked)
        self.clearButton.hide()

        self.backButtonText = 'Назад'
        self.backButton = QPushButton(self)
        self.backButton.setText(self.backButtonText)
        self.backButton.resize(self.backButton.sizeHint())
        self.backButton.move(self.leftMargin, self.height() - self.bottomMargin - self.backButton.height())
        self.backButton.clicked.connect(self.backButton_clicked)

        self.weightsLabelText = 'Веса данного вопроса для транспортных средств'
        self.weightsLabel = QLabel(self)
        self.weightsLabel.setText(self.weightsLabelText)
        self.weightsLabel.resize(self.weightsLabel.sizeHint())
        self.weightsLabel.move(self.leftMargin, self.deleteButtonY + self.deleteButtonHeight + self.betweenMargin)

        self.weightsTable = QTableWidget(self)
        self.weightsTable.setRowCount(1)
        self.weightsTable.setVerticalHeaderItem(0, QTableWidgetItem('Веса'))
        self.weightsTable.move(self.weightsLabel.x(), self.weightsLabel.y() + self.weightsLabel.height())
        self.weightsTable.resize(self.width() - self.leftMargin - self.rightMargin,
                                 self.backButton.y() - self.weightsTable.y())
        self.weightsTable.verticalHeader().setStretchLastSection(True)

        self.okButtonText = 'ОК'
        self.okButton = QPushButton(self)
        self.okButton.setText(self.okButtonText)
        self.okButton.resize(self.backButton.size())
        self.okButton.move(self.width() - self.rightMargin - self.okButton.width(), self.backButton.y())
        self.okButton.clicked.connect(self.okButton_clicked)

    def titleRefresh(self):
        self.title.setText(self.titleText % (self.currentQuestion+1))
        self.title.resize(self.title.sizeHint())
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

    def questionTextEditRefresh(self):
        self.questionTextEdit.setText(self.question.text if self.question.text is not None else '')

    def questionTipEditRefresh(self):
        self.questionTipEdit.setText(self.question.tip if self.question.tip is not None else '')

    def questionTypeComboBoxRefresh(self):
        self.questionTypeComboBox.setCurrentIndex(0 if self.question.type == 'range' else 1)

    def rangeBoundsLineEditRefresh(self):
        if self.question.type == 'range':
            self.rangeLeftBoundLineEdit.setText(str(self.question.lower_bound))
            self.rangeRightBoundLineEdit.setText(str(self.question.upper_bound))

    def discreteTableRefresh(self):
        if self.question.type == 'discrete':
            self.discreteTable.setColumnCount(len(self.question.answers))
            a_keys = list(self.question.answers.keys())
            for j in range(len(self.question.answers)):
                self.discreteTable.setItem(0, j, QTableWidgetItem(str(a_keys[j])))
                self.discreteTable.setItem(1, j, QTableWidgetItem(str(self.question.answers[a_keys[j]])))

    def weightsTableRefresh(self):
        self.weightsTable.setColumnCount(len(self.transport))
        for j in range(len(self.transport)):
            self.weightsTable.setHorizontalHeaderItem(j, QTableWidgetItem(self.transport[j][1]))
            self.weightsTable.setColumnWidth(j, (self.weightsTable.width() - self.weightsTable.verticalHeader().width())
                                             / len(self.transport))
            self.weightsTable.setItem(0, j, QTableWidgetItem(str(self.weights[j])))

    def refresh(self):
        self.titleRefresh()
        self.questionTextEditRefresh()
        self.questionTipEditRefresh()
        self.questionTypeComboBoxRefresh()
        self.rangeBoundsLineEditRefresh()
        self.discreteTableRefresh()
        self.weightsTableRefresh()

    # Метод перемещающий данную форму в центр экрана
    def moveToCenter(self):
        tmp_rectangle = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        tmp_rectangle.moveCenter(screen_center)
        self.move(tmp_rectangle.topLeft())

    @pyqtSlot()
    def addButton_clicked(self):
        self.hide()
        self.discreteTable.insertColumn(self.discreteTable.columnCount())
        self.discreteTable.setItem(0, self.discreteTable.columnCount()-1, QTableWidgetItem(''))
        self.discreteTable.setItem(1, self.discreteTable.columnCount()-1, QTableWidgetItem('0.0'))
        self.show()

    @pyqtSlot()
    def deleteButton_clicked(self):
        col_to_del = self.currentCol
        self.hide()
        self.discreteTable.removeColumn(col_to_del)
        self.show()

    @pyqtSlot()
    def clearButton_clicked(self):
        self.hide()
        while self.discreteTable.columnCount() > 0:
            self.discreteTable.removeColumn(0)
        self.show()

    @pyqtSlot()
    def backButton_clicked(self):
        closeMessageBox = QMessageBox(
            QMessageBox.Question,
            'Вы уверены?',
            'При переходе на предыдущую вкладку вся введенная информация будет утеряна!\nВы уверены, что хотите '
            'продолжить?')
        yesButton, noButton = \
            closeMessageBox.addButton('Да', QMessageBox.YesRole), \
            closeMessageBox.addButton('Нет', QMessageBox.NoRole)
        closeMessageBox.exec_()
        if closeMessageBox.clickedButton() == yesButton:
            self.hide()
            self.__init__(self.application, self.index)
            self.application.GUI[self.index-1].show()
        else:
            return

    @pyqtSlot()
    def okButton_clicked(self):
        self.question.text = self.questionTextEdit.toPlainText()
        self.question.tip = self.questionTipEdit.toPlainText()
        self.question.type = 'range' if self.questionTypeComboBox.currentIndex() == 0 else 'discrete'
        if self.question.type == 'range':
            try:
                self.question.lower_bound = int(self.rangeLeftBoundLineEdit.text())
                self.question.upper_bound = int(self.rangeRightBoundLineEdit.text())
            except ValueError:
                warningMessageBox = QMessageBox(
                    QMessageBox.Warning, 'Неверный формат!',
                    'Введенные значения для границ шкалы невозможно преобразовать в целые числа! '
                    'Пожалуйста, проверьте введенную информацию!',
                    QMessageBox.Ok
                )
                warningMessageBox.exec_()
                return
        elif self.question.type == 'discrete':
            try:
                _answers = {}
                for j in range(self.discreteTable.columnCount()):
                    col_index = j
                    key = self.discreteTable.item(0, j).text()
                    value = float(self.discreteTable.item(1, j).text())
                    _answers[key] = value
                self.question.answers = _answers.copy()
            except ValueError:
                warningMessageBox = QMessageBox(
                    QMessageBox.Warning, 'Неверный формат!',
                    'Данные введенные для столбца с индексом %d в таблице с ответами невозможно преобразовать к '
                    'верному формату! Пожалуйста, проверьте введенную информацию!' % (col_index+1),
                    QMessageBox.Ok
                )
                warningMessageBox.exec_()
                return
        try:
            _weights = []
            for j in range(self.weightsTable.columnCount()):
                col_index = j
                weight = float(self.weightsTable.item(0, j).text())
                _weights.append(weight)
            self.weights = _weights.copy()
        except:
            warningMessageBox = QMessageBox(
                QMessageBox.Warning, 'Неверный формат!',
                'Данные введенные для столбца с индексом %d в таблице с весами невозможно преобразовать к '
                'верному формату! Пожалуйста, проверьте введенную информацию!' % (col_index + 1),
                QMessageBox.Ok
            )
            warningMessageBox.exec_()
            return
        self.hide()
        self.application.GUI[self.index-1].questions[self.currentQuestion] = self.question.copy()
        self.application.GUI[self.index-1].weights[self.currentQuestion] = self.weights.copy()
        self.application.GUI[self.index-1].refreshTable()
        self.application.GUI[self.index-1].show()
        self.__init__(self.application, self.index)

    @pyqtSlot(int)
    def questionTypeComboBox_currentIndexChanged(self, index):
        self.hide()

        if index == 0:
            self.rangeLeftBoundLabel.show()
            self.rangeLeftBoundLineEdit.show()
            self.rangeRightBoundLabel.show()
            self.rangeRightBoundLineEdit.show()

            self.discreteLabel.hide()
            self.discreteTable.hide()
            self.addButton.hide()
            self.deleteButton.hide()
            self.clearButton.hide()

        elif index == 1:
            self.rangeLeftBoundLabel.hide()
            self.rangeLeftBoundLineEdit.hide()
            self.rangeRightBoundLabel.hide()
            self.rangeRightBoundLineEdit.hide()

            self.discreteLabel.show()
            self.discreteTable.show()
            self.addButton.show()
            self.deleteButton.show()
            self.clearButton.show()

        self.show()

    @pyqtSlot(int, int, int, int)
    def discreteTable_currentCellChanged(self, current_row, current_col, prev_row, prev_col):
        self.currentCol = current_col
        self.deleteButton.setEnabled(True)

    def closeEvent(self, event):
        closeMessageBox = QMessageBox(QMessageBox.Question, 'Вы уверены?', 'При закрытии приложения вся введенная '
                                                                           'информация будет утеряна!\nВы уверены, что '
                                                                           'хотите продолжить?')
        yesButton, noButton = \
            closeMessageBox.addButton('Да', QMessageBox.YesRole), \
            closeMessageBox.addButton('Нет', QMessageBox.NoRole)
        closeMessageBox.exec_()
        if closeMessageBox.clickedButton() == yesButton:
            event.accept()
        else:
            event.ignore()
