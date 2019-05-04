from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot


class ExpertChoiceWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)

        self.transport = None

        self.application = application
        self.index = index
        self_width, self_height = 350, 160
        self.resize(self_width, self_height)
        self.setFixedSize(self_width, self_height)
        self.moveToCenter()
        self.leftMargin, self.rightMargin, self.topMargin, self.bottomMargin, self.betweenMargin = \
            self_width * 0.02, self_width * 0.02, self_height * 0.05, self_height * 0.02, 20

        self.titleText = 'Пожалуйста, выберите раздел,\nкоторый вы хотите отредактировать.'
        # self.titleFont = QFont('Calibri', 14)
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        self.title.resize(self.title.sizeHint())
        # self.title.setFont(self.titleFont)
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

        self.transportButtonText = 'Виды транспорта'
        self.transportButton = QPushButton(self)
        self.transportButton.setText(self.transportButtonText)
        self.transportButtonX, self.transportButtonY = \
            self.leftMargin, \
            self.titleY + self.title.height() + self.betweenMargin
        self.transportButton.resize(self.width() - 2 * self.transportButtonX, self.transportButton.height())
        self.transportButton.move(self.transportButtonX, self.transportButtonY)
        self.transportButton.clicked.connect(self.transportButton_clicked)

        self.questionsButtonText = 'Вопросы'
        self.questionsButton = QPushButton(self)
        self.questionsButton.setText(self.questionsButtonText)
        self.questionsButton.resize(self.transportButton.width(), self.transportButton.height())
        self.questionsButtonX, self.questionsButtonY = \
            self.leftMargin, self.transportButtonY + self.transportButton.height() + \
            0.05 * self.betweenMargin
        self.questionsButton.move(self.questionsButtonX, self.questionsButtonY)
        self.questionsButton.clicked.connect(self.questionsButton_clicked)

        self.backButtonText = 'Назад'
        self.backButton = QPushButton(self)
        self.backButton.setText(self.backButtonText)
        self.backButtonX, self.backButtonY = \
            self.leftMargin, self.questionsButtonY + self.questionsButton.height() + 0.05 * self.betweenMargin
        self.backButton.resize(self.transportButton.width(), self.transportButton.height())
        self.backButton.move(self.backButtonX, self.backButtonY)
        self.backButton.clicked.connect(self.backButton_clicked)

        self.moveToCenter()

    # Метод перемещающий данную форму в центр экрана
    def moveToCenter(self):
        tmp_rectangle = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        tmp_rectangle.moveCenter(screen_center)
        self.move(tmp_rectangle.topLeft())

    @pyqtSlot()
    def transportButton_clicked(self):
        self.hide()
        self.application.GUI[self.application.transport_edit_index].show()

    @pyqtSlot()
    def backButton_clicked(self):
        self.hide()
        self.application.GUI[self.index-1].show()

    @pyqtSlot()
    def questionsButton_clicked(self):
        self.hide()
        self.application.GUI[self.application.questions_edit_index].show()
