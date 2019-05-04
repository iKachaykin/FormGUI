from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot


class ExpertOpeningWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)
        self.application = application
        self.index = index
        self_width, self_height = 290, 140
        self.resize(self_width, self_height)
        self.setFixedSize(self_width, self_height)
        self.moveToCenter()
        self.leftMargin, self.rightMargin, self.topMargin, self.bottomMargin, self.betweenMargin = \
            self_width * 0.02, self_width * 0.02, self_height * 0.05, self_height * 0.02, self_height * 0.05

        self.titleText = 'Как эксперту, вам предлагается внести\nвсе необходимые изменения в систему\nс целью её ' \
                         'найлучшей работы.'
        # self.titleFont = QFont('Calibri', 14)
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        # self.title.setFont(self.titleFont)
        self.titleX, self.titleY = 15, 10
        self.title.move(self.titleX, self.titleY)

        self.continueButtonText = 'ОК'
        self.continueButton = QPushButton(self)
        self.continueButton.setText(self.continueButtonText)
        self.continueButtonX, self.continueButtonY = 15, 70
        self.continueButton.resize(self.width() - 2 * self.continueButtonX, self.continueButton.height())
        self.continueButton.move(self.continueButtonX, self.continueButtonY)
        self.continueButton.clicked.connect(self.continueButton_clicked)

        self.backButtonText = 'Назад'
        self.backButton = QPushButton(self)
        self.backButton.setText(self.backButtonText)
        self.backButtonX, self.backButtonY = 15, 100
        self.backButton.resize(self.continueButton.width(), self.continueButton.height())
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
    def continueButton_clicked(self):
        self.hide()
        self.application.GUI[self.index+1].show()

    @pyqtSlot()
    def backButton_clicked(self):
        self.hide()
        self.application.GUI[0].show()
