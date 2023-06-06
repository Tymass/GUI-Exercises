import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot


class LoginWindow(QWidget):
    login_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("icon.png"))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label_username = QLabel("Username:")
        self.lineedit_username = QLineEdit()
        layout.addWidget(label_username)
        layout.addWidget(self.lineedit_username)

        label_password = QLabel("Password:")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password)
        layout.addWidget(self.lineedit_password)

        button_login = QPushButton("Login")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login)

        self.setLayout(layout)

    def login(self):
        username = self.lineedit_username.text()
        password = self.lineedit_password.text()

        self.login_signal.emit(username, password)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setWindowIcon(QIcon("icon.png"))

        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    @pyqtSlot(str, str)
    def check_login(self, username, password):
        try:
            with open("C:\\Users\\TymB\\GUI-Exercises\\fourth_project\\credentials.txt", "r") as file:
                for line in file:
                    if f"log: {username} psswd: {password}" in line:
                        self.label.setText("Logging was successful!")
                        QMessageBox.information(
                            self, "Success", "Logging was accurate!")
                        QApplication.quit()  # Close the application
                        return  # Exit the loop
                QMessageBox.warning(
                    self, "Error", "Invalid login credentials. Please try again.")
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Error", "Credentials file not found. Please make sure 'credentials.txt' exists.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    main_window = MainWindow()

    login_window.login_signal.connect(main_window.check_login)

    login_window.show()

    sys.exit(app.exec_())
