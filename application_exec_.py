from Project.UserExpertApplication import UserExpertApplication


if __name__ == '__main__':
    password = ''  # put your password here
    ue_app = UserExpertApplication('dbname=sai user=postgres password=%s' % password)
    ue_app.exec_()
