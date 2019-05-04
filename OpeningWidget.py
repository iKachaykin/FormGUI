from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot


# Класс, реализующий форму для ввода направления движения
class OpeningWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)
        self.application = application
        self.index = index
        self_width, self_height = 290, 200
        self.resize(self_width, self_height)
        self.setFixedSize(self_width, self_height)
        self.moveToCenter()
        self.leftMargin, self.rightMargin, self.topMargin, self.bottomMargin, self.betweenMargin = \
            self_width * 0.02, self_width * 0.02, self_height * 0.05, self_height * 0.02, self_height * 0.05

        self.titleText = 'Здравствуйте!\nДанная система помогает пользователю\nопределить, ' \
                         'каким видом транспорта\nвоспользоваться для переезда между\nнаселенными пунктами, ' \
                         'а эксперту -\nнастроить систему.' \
                         '\nПожалуйста, выберите кем вы являетесь!'
        # self.titleFont = QFont('Calibri', 14)
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        # self.title.setFont(self.titleFont)
        self.titleX, self.titleY = 15, 10
        self.title.move(self.titleX, self.titleY)

        self.userButtonText = 'Я - пользователь'
        self.userButton = QPushButton(self)
        self.userButton.setText(self.userButtonText)
        self.userButtonX, self.userButtonY = 15, 125
        self.userButton.resize(self.width() - 2 * self.userButtonX, self.userButton.height())
        self.userButton.move(self.userButtonX, self.userButtonY)
        self.userButton.clicked.connect(self.userButton_clicked)

        self.expertButtonText = 'Я - эксперт'
        self.expertButton = QPushButton(self)
        self.expertButton.setText(self.expertButtonText)
        self.expertButtonX, self.expertButtonY = 15, 155
        self.expertButton.resize(self.userButton.width(), self.userButton.height())
        self.expertButton.move(self.expertButtonX, self.expertButtonY)
        self.expertButton.clicked.connect(self.expertButton_clicked)

        self.moveToCenter()

    # Метод перемещающий данную форму в центр экрана
    def moveToCenter(self):
        tmp_rectangle = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        tmp_rectangle.moveCenter(screen_center)
        self.move(tmp_rectangle.topLeft())

    @pyqtSlot()
    def userButton_clicked(self):
        self.hide()
        self.application.GUI[self.application.user_index].show()

    @pyqtSlot()
    def expertButton_clicked(self):
        self.hide()
        self.application.GUI[self.application.expert_index].show()
