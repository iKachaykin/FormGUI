from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot


class UserResultWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)

        self.transport = None

        self.application = application
        self.index = index
        self_width, self_height = 350, 185
        self.resize(self_width, self_height)
        self.setFixedSize(self_width, self_height)
        self.moveToCenter()
        self.leftMargin, self.rightMargin, self.topMargin, self.bottomMargin, self.betweenMargin = \
            self_width * 0.02, self_width * 0.02, self_height * 0.05, self_height * 0.02, 20

        self.titleText = 'Результат работы системы'
        # self.titleFont = QFont('Calibri', 14)
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        self.title.resize(self.title.sizeHint())
        # self.title.setFont(self.titleFont)
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)
        
        self.optimalTransportText = 'Оптимальный вид транспорта: %s'
        self.optimalTransportLabel = QLabel(self)
        self.optimalTransportLabel.setText(self.optimalTransportText)
        self.optimalTransportLabel.resize(self.optimalTransportLabel.sizeHint())
        self.optimalTransportLabelX, self.optimalTransportLabelY = self.leftMargin, self.titleY + self.betweenMargin
        self.optimalTransportLabel.move(self.optimalTransportLabelX, self.optimalTransportLabelY)
        
        self.optimalTransportDescriptionText = 'Описание: %s'
        self.optimalTransportDescriptionLabel = QLabel(self)
        self.optimalTransportDescriptionLabel.setText(self.optimalTransportDescriptionText)
        self.optimalTransportDescriptionLabel.resize(self.optimalTransportDescriptionLabel.sizeHint())
        self.optimalTransportDescriptionLabelX, self.optimalTransportDescriptionLabelY = \
            self.leftMargin, self.optimalTransportLabelY + self.betweenMargin
        self.optimalTransportDescriptionLabel.move(self.optimalTransportDescriptionLabelX,
                                                   self.optimalTransportDescriptionLabelY)

        self.exitButtonText = 'Выход'
        self.exitButton = QPushButton(self)
        self.exitButton.setText(self.exitButtonText)
        self.exitButtonX, self.exitButtonY = \
            self.leftMargin, \
            self.optimalTransportDescriptionLabelY + self.optimalTransportDescriptionLabel.height() + \
            self.betweenMargin
        self.exitButton.resize(self.width() - 2 * self.exitButtonX, self.exitButton.height())
        self.exitButton.move(self.exitButtonX, self.exitButtonY)
        self.exitButton.clicked.connect(self.exitButton_clicked)

        self.backButtonText = 'Назад'
        self.backButton = QPushButton(self)
        self.backButton.setText(self.backButtonText)
        self.backButtonX, self.backButtonY = self.leftMargin, self.exitButtonY + self.exitButton.height() + \
                                             0.05 * self.betweenMargin
        self.backButton.resize(self.exitButton.width(), self.exitButton.height())
        self.backButton.move(self.backButtonX, self.backButtonY)
        self.backButton.clicked.connect(self.backButton_clicked)

        self.toOpeningButtonText = 'В начало'
        self.toOpeningButton = QPushButton(self)
        self.toOpeningButton.setText(self.toOpeningButtonText)
        self.toOpeningButton.resize(self.exitButton.width(), self.exitButton.height())
        self.toOpeningButtonX, self.toOpeningButtonY = \
            self.leftMargin, self.backButtonY + self.backButton.height() + \
            0.05 * self.betweenMargin
        self.toOpeningButton.move(self.toOpeningButtonX, self.toOpeningButtonY)
        self.toOpeningButton.clicked.connect(self.toOpeningButton_clicked)

        self.moveToCenter()

    # Метод перемещающий данную форму в центр экрана
    def moveToCenter(self):
        tmp_rectangle = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        tmp_rectangle.moveCenter(screen_center)
        self.move(tmp_rectangle.topLeft())

    def setTransport(self, transport):
        self.transport = transport

        self.optimalTransportText = 'Оптимальный вид транспорта: %s' % transport[1]
        self.optimalTransportLabel.setText(self.optimalTransportText)
        self.optimalTransportLabel.resize(self.optimalTransportLabel.sizeHint())
        self.optimalTransportLabelX, self.optimalTransportLabelY = self.leftMargin, self.titleY + self.betweenMargin
        self.optimalTransportLabel.move(self.optimalTransportLabelX, self.optimalTransportLabelY)

        if transport[2] is not None:
            self.optimalTransportDescriptionText = 'Описание: %s' % \
                                                   (transport[2] if transport[2] != '' else 'отсутствует')
        else:
            self.optimalTransportDescriptionText = ''
        self.optimalTransportDescriptionLabel.setText(self.optimalTransportDescriptionText)
        self.optimalTransportDescriptionLabel.resize(self.optimalTransportDescriptionLabel.sizeHint())
        self.optimalTransportDescriptionLabelX, self.optimalTransportDescriptionLabelY = \
            self.leftMargin, self.optimalTransportLabelY + self.betweenMargin
        self.optimalTransportDescriptionLabel.move(self.optimalTransportDescriptionLabelX,
                                                   self.optimalTransportDescriptionLabelY)

    @pyqtSlot()
    def exitButton_clicked(self):
        closeMessageBox = QMessageBox(QMessageBox.Question, 'Вы уверены?', 'При закрытии приложения вся введенная '
                                                                           'информация будет утеряна!\nВы уверены, что '
                                                                           'хотите продолжить?')
        yesButton, noButton = \
            closeMessageBox.addButton('Да', QMessageBox.YesRole), \
            closeMessageBox.addButton('Нет', QMessageBox.NoRole)
        closeMessageBox.exec_()
        if closeMessageBox.clickedButton() == yesButton:
            QApplication.quit()
        else:
            return

    @pyqtSlot()
    def backButton_clicked(self):
        self.hide()
        self.application.GUI[self.index-1].show()
        self.application.GUI[self.index-1].backButton_clicked()

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
            self.application.GUI[self.index - 1].__init__(self.application, self.index-1)
            self.application.GUI[0].show()
