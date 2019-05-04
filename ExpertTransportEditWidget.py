from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt


class ExpertTransportEditWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)
        self.application = application
        self.index = index
        width_multiplier, height_multiplier = 0.4, 0.4
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
        self.rowToDel = -1

        self.titleText = 'Редактор видов транспорта'
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        self.title.resize(self.title.sizeHint())
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

        self.transportTable = QTableWidget(self)
        self.transportTableX, self.transportTableY = \
            self.leftMargin, self.titleY + self.title.height() + self.betweenMargin
        self.transportTable.move(self.transportTableX, self.transportTableY)
        self.transportTableWidth, self.transportTableHeight = 0.75 * self.width(), 0.7 * self.height()
        self.transportTable.resize(self.transportTableWidth, self.transportTableHeight)
        self.transportTable.setColumnCount(3)
        self.transportTable.setRowCount(len(self.transport))
        self.transportTable.setHorizontalHeaderItem(0, QTableWidgetItem('№'))
        self.transportTable.setHorizontalHeaderItem(1, QTableWidgetItem('Название'))
        self.transportTable.setHorizontalHeaderItem(2, QTableWidgetItem('Описание'))
        self.transportTable.horizontalHeader().setStretchLastSection(True)
        self.transportTable.verticalHeader().hide()
        for i in range(len(self.transport)):
            for j in range(3):
                cell_i_j = QTableWidgetItem(str(self.transport[i][j]))
                if j == 0:
                    cell_i_j.setFlags(cell_i_j.flags() ^ Qt.ItemIsEditable ^ Qt.ItemIsSelectable)
                self.transportTable.setItem(i, j, cell_i_j)
        self.transportTable.currentCellChanged.connect(self.transportTable_currentCellChanged)

        self.addButtonText = 'Добавить'
        self.addButton = QPushButton(self)
        self.addButton.setText(self.addButtonText)
        self.addButtonX, self.addButtonY = \
            self.transportTableX + self.transportTableWidth + self.betweenMargin, self.transportTableY
        self.addButtonWidth, self.addButtonHeight = \
            self.width() - self.leftMargin - self.betweenMargin - self.rightMargin - self.transportTableWidth, \
            self.addButton.sizeHint().height()
        self.addButton.move(self.addButtonX, self.addButtonY)
        self.addButton.resize(self.addButtonWidth, self.addButtonHeight)
        self.addButton.clicked.connect(self.addButton_clicked)

        self.deleteButtonText = 'Удалить'
        self.deleteButton = QPushButton(self)
        self.deleteButton.setText(self.deleteButtonText)
        self.deleteButtonX, self.deleteButtonY = \
            self.addButtonX, self.addButtonY + self.addButtonHeight + self.betweenMargin
        self.deleteButtonWidth, self.deleteButtonHeight = self.addButtonWidth, self.addButtonHeight
        self.deleteButton.move(self.deleteButtonX, self.deleteButtonY)
        self.deleteButton.resize(self.deleteButtonWidth, self.deleteButtonHeight)
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteButton_clicked)

        self.clearButtonText = 'Очистить'
        self.clearButton = QPushButton(self)
        self.clearButton.setText(self.clearButtonText)
        self.clearButtonX, self.clearButtonY = \
            self.deleteButtonX, self.deleteButtonY + self.deleteButtonHeight + self.betweenMargin
        self.clearButtonWidth, self.clearButtonHeight = self.deleteButtonWidth, self.deleteButtonHeight
        self.clearButton.move(self.clearButtonX, self.clearButtonY)
        self.clearButton.resize(self.clearButtonWidth, self.clearButtonHeight)
        self.clearButton.clicked.connect(self.clearButton_clicked)

        self.backButtonText = 'Назад'
        self.backButton = QPushButton(self)
        self.backButton.setText(self.backButtonText)
        self.backButtonX, self.backButtonY = \
            self.leftMargin, self.transportTableY + self.transportTableHeight + self.betweenMargin
        self.backButtonWidth, self.backButtonHeight = \
            (self.width() - self.leftMargin - self.rightMargin - 2 * self.betweenMargin) / 3, \
            self.backButton.sizeHint().height()
        self.backButton.move(self.backButtonX, self.backButtonY)
        self.backButton.resize(self.backButtonWidth, self.backButtonHeight)
        self.backButton.clicked.connect(self.backButton_clicked)

        self.toOpeningButtonText = 'В начало'
        self.toOpeningButton = QPushButton(self)
        self.toOpeningButton.setText(self.toOpeningButtonText)
        self.toOpeningButtonX, self.toOpeningButtonY = \
            self.backButtonX + self.backButtonWidth + self.betweenMargin, self.backButtonY
        self.toOpeningButtonWidth, self.toOpeningButtonHeight = self.backButtonWidth, self.backButtonHeight
        self.toOpeningButton.move(self.toOpeningButtonX, self.toOpeningButtonY)
        self.toOpeningButton.resize(self.toOpeningButtonWidth, self.toOpeningButtonHeight)
        self.toOpeningButton.clicked.connect(self.toOpeningButton_clicked)

        self.applyButtonText = 'Применить'
        self.applyButton = QPushButton(self)
        self.applyButton.setText(self.applyButtonText)
        self.applyButtonX, self.applyButtonY = \
            self.toOpeningButtonX + self.toOpeningButtonWidth + self.betweenMargin, self.toOpeningButtonY
        self.applyButtonWidth, self.applyButtonHeight = self.toOpeningButtonWidth, self.toOpeningButtonHeight
        self.applyButton.move(self.applyButtonX, self.applyButtonY)
        self.applyButton.resize(self.applyButtonWidth, self.applyButtonHeight)
        self.applyButton.clicked.connect(self.applyButton_clicked)

    # Метод перемещающий данную форму в центр экрана
    def moveToCenter(self):
        tmp_rectangle = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        tmp_rectangle.moveCenter(screen_center)
        self.move(tmp_rectangle.topLeft())

    @pyqtSlot()
    def addButton_clicked(self):
        self.transportTable.insertRow(self.transportTable.rowCount())
        cell_i_0 = QTableWidgetItem(str(self.transportTable.rowCount()))
        cell_i_0.setFlags(cell_i_0.flags() ^ Qt.ItemIsEditable ^ Qt.ItemIsSelectable)

        self.transportTable.setItem(self.transportTable.rowCount()-1, 0, cell_i_0)
        self.transportTable.setItem(self.transportTable.rowCount()-1, 1, QTableWidgetItem(''))
        self.transportTable.setItem(self.transportTable.rowCount()-1, 2, QTableWidgetItem(''))

        for i in range(len(self.weights)):
            self.weights[i].append(0.0)

    @pyqtSlot()
    def deleteButton_clicked(self):
        row_to_del = self.rowToDel
        if self.transportTable.rowCount() > 1:
            for i in range(row_to_del+1, self.transportTable.rowCount()):
                cell_i_0_prev_value = int(self.transportTable.item(i, 0).text())
                cell_i_0_new = QTableWidgetItem(str(cell_i_0_prev_value - 1))
                self.transportTable.setItem(i, 0, cell_i_0_new)
        self.transportTable.removeRow(row_to_del)
        try:
            for i in range(len(self.weights)):
                self.weights[i].pop(row_to_del)
        except IndexError:
            for i in range(len(self.weights)):
                self.weights[i].clear()

    @pyqtSlot()
    def clearButton_clicked(self):
        while self.transportTable.rowCount() != 0:
            self.transportTable.removeRow(0)
        for i in range(len(self.weights)):
            self.weights[i].clear()

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
            self.application.GUI[self.application.expert_choice_index].show()
        else:
            return

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
        else:
            return

    @pyqtSlot()
    def applyButton_clicked(self):
        applyMessageBox = QMessageBox(
            QMessageBox.Question,
            'Вы уверены?',
            'Вы уверены, что хотите применить введенные изменения?')
        yesButton, noButton = \
            applyMessageBox.addButton('Да', QMessageBox.YesRole), \
            applyMessageBox.addButton('Нет', QMessageBox.NoRole)
        applyMessageBox.exec_()
        if applyMessageBox.clickedButton() == yesButton:
            self.transport.clear()
            for i in range(self.transportTable.rowCount()):
                transport_tmp = (
                    int(self.transportTable.item(i, 0).text()),
                    self.transportTable.item(i, 1).text(),
                    self.transportTable.item(i, 2).text()
                )
                self.transport.append(transport_tmp)
            self.application.logic.setWeightsAndTransport(self.weights, self.transport)
            doneMessageBox = QMessageBox(
                QMessageBox.Information,
                'Готово',
                'Изменения применены'
            )
            okButton = doneMessageBox.addButton('ОК', QMessageBox.AcceptRole)
            doneMessageBox.exec_()
            if doneMessageBox.clickedButton() == okButton:
                self.hide()
                self.__init__(self.application, self.index)
                self.application.GUI[self.application.expert_choice_index].show()
        else:
            return


    @pyqtSlot(int, int, int, int)
    def transportTable_currentCellChanged(self, current_row, current_col, prev_row, prev_col):
        if current_col == 0:
            self.deleteButton.setEnabled(False)
            self.rowToDel = -1
        else:
            self.deleteButton.setEnabled(True)
            self.rowToDel = current_row

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
