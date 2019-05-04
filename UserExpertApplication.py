import sys
from PyQt5.QtWidgets import QApplication
from Project.LogicTier import LogicTier
from Project.OpeningWidget import OpeningWidget
from Project.UserFormWidget import UserFormWidget
from Project.UserResultWidget import UserResultWidget
from Project.UserOpeningWidget import UserOpeningWidget
from Project.ExpertChoiceWidget import ExpertChoiceWidget
from Project.ExpertOpeningWidget import ExpertOpeningWidget
from Project.ExpertTransportEditWidget import ExpertTransportEditWidget
from Project.ExpertQuestionsEditWidget import ExpertQuestionsEditWidget
from Project.ExpertQuestionsEditButtonWidget import ExpertQuestionsEditButtonWidget


# Класс, реализующий приложение пользователя/эксперта
class UserExpertApplication:

    # Конструктор
    def __init__(self, localhost):
        self.localhost = localhost
        self.logic = LogicTier(localhost)
        self.app = QApplication(sys.argv)
        self.GUI = [OpeningWidget(self, 0), UserOpeningWidget(self, 1), UserFormWidget(self, 2),
                    UserResultWidget(self, 3), ExpertOpeningWidget(self, 4), ExpertChoiceWidget(self, 5),
                    ExpertTransportEditWidget(self, 6), ExpertQuestionsEditWidget(self, 7),
                    ExpertQuestionsEditButtonWidget(self, 8)]
        self.GUI[0].show()
        for i in range(1, len(self.GUI)):
            self.GUI[i].hide()
        self.user_index = 1
        self.expert_index = 4
        self.expert_choice_index = 5
        self.transport_edit_index = 6
        self.questions_edit_index = 7

    # Запуск приложения
    def exec_(self):
        sys.exit(self.app.exec_())
