from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip, QProgressBar, QSlider, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt

eps = 1e-52


class UserFormWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)
        self.application = application
        self.index = index
        width_multiplier, height_multiplier = 0.4, 0.2
        self_width, self_height = QDesktopWidget().availableGeometry().width() * width_multiplier, \
                                  QDesktopWidget().availableGeometry().height() * height_multiplier
        self.resize(self_width, self_height)
        self.setFixedSize(self_width, self_height)
        self.moveToCenter()
        self.leftMargin, self.rightMargin, self.topMargin, self.bottomMargin, self.betweenMargin = \
            self_width * 0.02, self_width * 0.02, self_height * 0.05, self_height * 0.02, self_height * 0.05

        self.questions = self.application.logic.getQuestions()
        self.transport = self.application.logic.getTransport()
        self.weights = self.application.logic.getWeights(len(self.questions), len(self.transport))
        self.marks = [0.0 for j in range(len(self.transport))]
        self.all_marks = [self.marks.copy()]

        self.indexOfQuestion = 0

        self.titleText = 'Вопрос %d из %d' % (self.indexOfQuestion+1, len(self.questions))
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        self.title.resize(self.title.sizeHint())
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

        self.progress = QProgressBar(self)
        self.progressX, self.progressY = self.leftMargin, self.titleY + 10
        self.progressWidth, self.progressHeight = self.width() - 2*self.progressX, self.progress.height()
        self.progress.move(self.progressX, self.progressY)
        self.progress.resize(self.progressWidth, self.progressHeight)
        self.progress.setMinimum(0)
        self.progress.setMaximum(len(self.questions)-1)

        self.questionLabel = QLabel(self)
        self.questionLabelX, self.questionLabelY = \
            (self.width() - self.questionLabel.width()) / 2, self.progressY + 30
        self.questionLabelRefresh()

        self.answerComboBox = QComboBox(self)
        self.answerComboBoxX, self.answerComboBoxY = \
            (self.width() - self.answerComboBox.width()) / 2, self.questionLabelY + 20
        self.answerComboBoxRefresh()

        self.answerSliderLabels = []

        self.answerSlider = QSlider(self)
        self.answerSliderWidth, self.answerSliderHeight = \
            self.width() - 2*self.leftMargin, self.answerSlider.height()
        self.answerSlider.resize(self.answerSliderWidth, self.answerSliderHeight)
        self.answerSliderX, self.answerSliderY = self.leftMargin, self.questionLabelY + 20
        self.answerSlider.move(self.answerSliderX, self.answerSliderY)
        self.answerSlider.setOrientation(Qt.Horizontal)
        self.answerSlider.setTickPosition(QSlider.TicksBelow)
        self.answerSliderRefresh()

        self.backButtonText = 'Назад'
        self.backButton = QPushButton(self)
        self.backButton.setText(self.backButtonText)
        self.backButtonX, self.backButtonY = self.leftMargin - 6, 130
        self.backButton.move(self.backButtonX, self.backButtonY)
        self.backButton.clicked.connect(self.backButton_clicked)

        self.continueButtonText = 'Далее'
        self.continueButton = QPushButton(self)
        self.continueButton.setText(self.continueButtonText)
        self.continueButtonX, self.continueButtonY = \
            self.progressWidth + self.progress.x() - self.continueButton.width() + 24, 130
        self.continueButton.move(self.continueButtonX, self.continueButtonY)
        self.continueButton.clicked.connect(self.continueButton_clicked)

        self.toOpeningButtonText = 'В начало'
        self.toOpeningButton = QPushButton(self)
        self.toOpeningButton.setText(self.toOpeningButtonText)
        self.toOpeningButton.resize(self.toOpeningButton.sizeHint().width()+40,
                                    self.toOpeningButton.sizeHint().height())
        self.toOpeningButtonX, self.toOpeningButtonY = \
            self.backButton.x() + self.backButton.width() + \
            (self.continueButton.x() - (self.backButton.x() + self.backButton.width())) / 2 - \
            self.toOpeningButton.width() / 2, 130
        self.toOpeningButton.move(self.toOpeningButtonX, self.toOpeningButtonY)
        self.toOpeningButton.clicked.connect(self.toOpeningButton_clicked)

        self.moveToCenter()

    # Метод перемещающий данную форму в центр экрана
    def moveToCenter(self):
        tmp_rectangle = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        tmp_rectangle.moveCenter(screen_center)
        self.move(tmp_rectangle.topLeft())

    def titleRefresh(self):
        self.titleText = 'Вопрос %d из %d' % (self.indexOfQuestion+1, len(self.questions))
        self.title.setText(self.titleText)
        self.title.resize(self.title.sizeHint())
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

    def progressUpdate(self):
        self.progress.setValue(self.indexOfQuestion)

    def questionLabelRefresh(self):
        self.questionLabel.setText(self.questions[self.indexOfQuestion].text)
        self.questionLabel.resize(self.questionLabel.sizeHint())
        self.questionLabelX, self.questionLabelY = \
            (self.width() - self.questionLabel.width()) / 2, self.progressY + 30
        self.questionLabel.move(self.questionLabelX, self.questionLabelY)
        if self.questions[self.indexOfQuestion].tip is not None and self.questions[self.indexOfQuestion].tip != '':
            self.questionLabel.setToolTip(self.questions[self.indexOfQuestion].tip)

    def answerComboBoxRefresh(self):
        if self.questions[self.indexOfQuestion].type == 'discrete':
            self.answerComboBox.clear()
            self.answerComboBox.addItems(self.questions[self.indexOfQuestion].answers.keys())
            self.answerComboBox.resize(self.answerComboBox.sizeHint().width()+10,
                                       self.answerComboBox.sizeHint().height())
            self.answerComboBoxX, self.answerComboBoxY = \
                (self.width() - self.answerComboBox.width()) / 2, self.questionLabelY + 20
            self.answerComboBox.move(self.answerComboBoxX, self.answerComboBoxY)
            self.answerComboBox.show()
        else:
            self.answerComboBox.hide()

    def answerSliderRefresh(self):
        if self.questions[self.indexOfQuestion].type == 'range':
            for i in range(len(self.answerSliderLabels)):
                self.answerSliderLabels[i].hide()
            self.answerSliderLabels.clear()
            self.answerSlider.setRange(self.questions[self.indexOfQuestion].lower_bound,
                                       self.questions[self.indexOfQuestion].upper_bound)
            self.answerSlider.setTickInterval(1)
            self.answerSlider.setSingleStep(1)
            initial_point_x = self.answerSlider.x() + 5
            shift = (self.answerSlider.width() - 17.5) / \
                    (self.questions[self.indexOfQuestion].upper_bound -
                     self.questions[self.indexOfQuestion].lower_bound)

            for i in range(self.questions[self.indexOfQuestion].lower_bound,
                           self.questions[self.indexOfQuestion].upper_bound+1):
                self.answerSliderLabels.append(QLabel(self))
                self.answerSliderLabels[-1].setText('%d' % i)
                self.answerSliderLabels[-1].move(initial_point_x + shift * i, self.answerSlider.y() + 30)
                self.answerSliderLabels[-1].show()
            self.answerSlider.show()
        else:
            self.answerSlider.hide()
            for i in range(len(self.answerSliderLabels)):
                self.answerSliderLabels[i].hide()

    def marksUpdate(self):
        answer_current = 0.0
        if self.questions[self.indexOfQuestion].type == 'discrete':
            answer_current = self.questions[self.indexOfQuestion].answers[self.answerComboBox.currentText()]
        elif self.questions[self.indexOfQuestion].type == 'range':
            answer_current = self.answerSlider.value()
        for j in range(len(self.transport)):
            if self.marks[j] < -eps:
                continue
            if self.weights[self.indexOfQuestion][j] * answer_current < -eps:
                self.marks[j] = -1.0
            else:
                self.marks[j] = self.marks[j] + self.weights[self.indexOfQuestion][j] * answer_current
        self.all_marks.append(self.marks.copy())

    def refresh(self):
        self.hide()
        self.titleRefresh()
        self.questionLabelRefresh()
        self.answerComboBoxRefresh()
        self.answerSliderRefresh()
        self.show()

    @pyqtSlot()
    def continueButton_clicked(self):
        self.marksUpdate()
        self.indexOfQuestion += 1
        self.progressUpdate()
        if self.indexOfQuestion < len(self.questions):
            self.questionLabel.clear()
            self.refresh()
        else:
            self.application.GUI[self.index+1].show()
            solution_index = self.marks.index(max(self.marks))
            if self.marks[solution_index] > -eps:
                self.application.GUI[self.index+1].setTransport(self.transport[solution_index])
            else:
                self.application.GUI[self.index+1].setTransport(
                    (None, 'кажется, между\nнаселенными пунктами нет транспортного\nсоединения...', None)
                )
            self.hide()

    @pyqtSlot()
    def backButton_clicked(self):
        self.indexOfQuestion -= 1
        if self.indexOfQuestion >= 0:
            self.refresh()
            self.progressUpdate()
            self.all_marks.pop()
            self.marks = self.all_marks[-1].copy()
        else:
            self.toOpeningButton_clicked()

    @pyqtSlot()
    def toOpeningButton_clicked(self):
        closeMessageBox = QMessageBox(QMessageBox.Question, 'Вы уверены?', 'При возврате в начало вся введенная '
                                                                           'информация будет утеряна!\nВы уверены, что '
                                                                           'хотите продолжить?')
        yesButton, noButton = \
            closeMessageBox.addButton('Да', QMessageBox.YesRole), \
            closeMessageBox.addButton('Нет', QMessageBox.NoRole)
        closeMessageBox.exec_()
        if closeMessageBox.clickedButton() == yesButton:
            self.hide()
            self.__init__(self.application, self.index)
            self.application.GUI[0].show()

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
