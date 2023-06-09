from PyQt5.QtWidgets import QApplication
import sys
from logging_lobby import LoginWindow

if __name__ == "__main__":
    open('fourth_project/logs/temp_log.txt', 'w').close()
    open('fourth_project/logs/shaft_log.txt', 'w').close()
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
