from PyQt5.QtWidgets import QApplication
import sys
from logging_lobby import LoginWindow1, LoginWindow2

if __name__ == "__main__":
    open('engine_data.txt', 'w').close()
    app = QApplication(sys.argv)

    login_window = LoginWindow1()
    main_window = LoginWindow2()

    login_window.login_signal.connect(main_window.check_login)

    login_window.show()

    sys.exit(app.exec_())
