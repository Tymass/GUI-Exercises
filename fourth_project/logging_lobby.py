import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("icon.png"))
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        self.lineedit_username = QLineEdit()
        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.lineedit_username)

        self.label_password = QLabel("Password:")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.lineedit_password)

        self.label_line_nr = QLabel("Line number:")
        self.lineedit_line_nr = QLineEdit()
        self.layout.addWidget(self.label_line_nr)
        self.layout.addWidget(self.lineedit_line_nr)

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login)
        self.layout.addWidget(self.button_login)

        self.setLayout(self.layout)

    def login(self):
        username = self.lineedit_username.text()
        password = self.lineedit_password.text()
        line_nr = self.lineedit_line_nr.text()

        try:
            with open("credentials.txt", "r") as file:
                for line in file:
                    if f"log: {username} psswd: {password} line: {line_nr}" in line:
                        self.post_login_ui()
                        return
            QMessageBox.warning(
                self, "Error", "Invalid login credentials. Please try again.")
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Error", "Credentials file not found. Please make sure 'credentials.txt' exists.")

    def post_login_ui(self):
        # clear the layout first
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        # set new UI
        self.label = QLabel("Logging was successful!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        QMessageBox.information(self, "Success", "Logging was accurate!")

        # If you want to show another window after login, uncomment below lines
        # self.main = CustomMainWindow()
        # self.main.show()
        # self.close()


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
