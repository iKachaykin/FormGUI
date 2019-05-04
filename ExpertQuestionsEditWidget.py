from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QSpinBox, QPushButton, QMessageBox, QComboBox,
                             QLabel, QToolTip, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from Project.Question import Question


class ExpertQuestionsEditWidget(QWidget):

    # Конструктор
    def __init__(self, application, index, parent=None):
        super().__init__(parent)
        self.application = application
        self.index = index
        width_multiplier, height_multiplier = 0.7, 0.4
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
        self.rowCurrent = -1

        self.titleText = 'Редактор вопросов'
        self.title = QLabel(self)
        self.title.setText(self.titleText)
        self.title.resize(self.title.sizeHint())
        self.titleX, self.titleY = (self.width() - self.title.width()) / 2, self.topMargin
        self.title.move(self.titleX, self.titleY)

        self.questionsTable = QTableWidget(self)
        self.questionsTableX, self.questionsTableY = \
            self.leftMargin, self.titleY + self.title.height() + self.betweenMargin
        self.questionsTable.move(self.questionsTableX, self.questionsTableY)
        self.questionsTableWidth, self.questionsTableHeight = 0.7 * self.width(), 0.7 * self.height()
        self.questionsTable.resize(self.questionsTableWidth, self.questionsTableHeight)
        self.questionsTable.setColumnCount(2)
        self.questionsTable.setRowCount(len(self.questions))
        self.questionsTable.setHorizontalHeaderItem(0, QTableWidgetItem('№'))
        self.questionsTable.setHorizontalHeaderItem(1, QTableWidgetItem('Вопрос'))
        self.questionsTable.horizontalHeader().setStretchLastSection(True)
        self.questionsTable.verticalHeader().hide()
        for i in range(len(self.questions)):
            cell_i_id = QTableWidgetItem(str(self.questions[i].id))
            cell_i_id.setFlags(cell_i_id.flags() ^ Qt.ItemIsEditable ^ Qt.ItemIsSelectable)
            self.questionsTable.setItem(i, 0, cell_i_id)
    
            cell_i_text = QTableWidgetItem(str(self.questions[i].text))
            cell_i_text.setFlags(cell_i_text.flags() ^ Qt.ItemIsEditable)
            self.questionsTable.setItem(i, 1, cell_i_text)

        self.questionsTable.currentCellChanged.connect(self.questionsTable_currentCellChanged)
        
        self.editButtonText = 'Редактировать'
        self.editButton = QPushButton(self)
        self.editButton.setText(self.editButtonText)
        self.editButtonX, self.editButtonY = \
            self.questionsTableX + self.questionsTableWidth + self.betweenMargin, self.questionsTableY
        self.editButtonWidth, self.editButtonHeight = \
            self.width() - self.leftMargin - self.betweenMargin - self.rightMargin - self.questionsTableWidth, \
            self.editButton.sizeHint().height()
        self.editButton.move(self.editButtonX, self.editButtonY)
        self.editButton.resize(self.editButtonWidth, self.editButtonHeight)
        self.editButton.setEnabled(False)
        self.editButton.clicked.connect(self.editButton_clicked)

        self.addButtonText = 'Добавить'
        self.addButton = QPushButton(self)
        self.addButton.setText(self.addButtonText)
        self.addButtonX, self.addButtonY = \
            self.editButtonX, self.editButtonY + self.editButtonHeight + self.betweenMargin
        self.addButtonWidth, self.addButtonHeight = \
            self.width() - self.leftMargin - self.betweenMargin - self.rightMargin - self.questionsTableWidth, \
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
            self.leftMargin, self.questionsTableY + self.questionsTableHeight + self.betweenMargin
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

    def refreshTable(self):
        for i in range(len(self.questions)):
            cell_i_id = QTableWidgetItem(str(self.questions[i].id))
            cell_i_id.setFlags(cell_i_id.flags() ^ Qt.ItemIsEditable ^ Qt.ItemIsSelectable)
            self.questionsTable.setItem(i, 0, cell_i_id)

            cell_i_text = QTableWidgetItem(str(self.questions[i].text))
            cell_i_text.setFlags(cell_i_text.flags() ^ Qt.ItemIsEditable)
            self.questionsTable.setItem(i, 1, cell_i_text)

    @pyqtSlot()
    def editButton_clicked(self):
        question_to_edit = self.rowCurrent
        self.hide()
        self.application.GUI[self.index+1].currentQuestion = question_to_edit
        self.application.GUI[self.index+1].question = self.questions[question_to_edit].copy()
        self.application.GUI[self.index+1].transport = self.transport.copy()
        self.application.GUI[self.index+1].weights = self.weights[question_to_edit].copy()
        self.application.GUI[self.index+1].refresh()
        self.application.GUI[self.index+1].show()

    @pyqtSlot()
    def addButton_clicked(self):
        self.questionsTable.insertRow(self.questionsTable.rowCount())

        cell_i_id = QTableWidgetItem(str(self.questionsTable.rowCount()))
        cell_i_id.setFlags(cell_i_id.flags() ^ Qt.ItemIsEditable ^ Qt.ItemIsSelectable)
        self.questionsTable.setItem(self.questionsTable.rowCount()-1, 0, cell_i_id)

        cell_i_text = QTableWidgetItem('')
        cell_i_text.setFlags(cell_i_text.flags() ^ Qt.ItemIsEditable)
        self.questionsTable.setItem(self.questionsTable.rowCount()-1, 1, cell_i_text)

        self.weights.append([0.0 for j in range(len(self.transport))])
        question_tmp = Question(self.questionsTable.rowCount(), '', '', 'range')
        question_tmp.lower_bound = 0
        question_tmp.upper_bound = 10
        question_tmp.answers = {}
        self.questions.append(question_tmp)

    @pyqtSlot()
    def deleteButton_clicked(self):
        row_to_del = self.rowCurrent
        if self.questionsTable.rowCount() > 1:
            for i in range(row_to_del+1, self.questionsTable.rowCount()):
                cell_i_0_prev_value = int(self.questionsTable.item(i, 0).text())
                cell_i_0_new = QTableWidgetItem(str(cell_i_0_prev_value - 1))
                self.questionsTable.setItem(i, 0, cell_i_0_new)
                self.questions[i].id -= 1
        self.questionsTable.removeRow(row_to_del)
        if len(self.questions) > 0:
            self.questions.pop(row_to_del)
        try:
            self.weights.pop(row_to_del)
        except IndexError:
            for i in range(len(self.weights)):
                self.weights[i].clear()
        self.hide()
        self.show()

    @pyqtSlot()
    def clearButton_clicked(self):
        while self.questionsTable.rowCount() != 0:
            self.questionsTable.removeRow(0)
        self.weights.clear()
        self.questions.clear()

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
            self.application.logic.setWeightsAndQuestions(self.weights, self.questions)
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
    def questionsTable_currentCellChanged(self, current_row, current_col, prev_row, prev_col):
        if current_col == 0:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.rowCurrent = -1
        else:
            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            self.rowCurrent = current_row

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
