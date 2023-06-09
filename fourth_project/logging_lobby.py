from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from app_window import CustomMainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("fourth_project/sources/icon.png"))
        self.setup_ui()

    def setup_ui(self):
        self.camera_on = False

        self.rb_on = QRadioButton("On", self)
        self.rb_off = QRadioButton("Off", self)
        self.rb_off.setChecked(True)
        self.rb_on.clicked.connect(self.turn_camera_on)
        self.rb_off.clicked.connect(self.turn_camera_off)

        self.radio_layout = QVBoxLayout()
        self.radio_layout.addWidget(
            QLabel("Show camera view?"), alignment=Qt.AlignTop)
        self.radio_layout.addWidget(self.rb_on, alignment=Qt.AlignTop)
        self.radio_layout.addWidget(self.rb_off, alignment=Qt.AlignTop)

        self.v_layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        self.lineedit_username = QLineEdit()
        self.v_layout.addWidget(self.label_username)
        self.v_layout.addWidget(self.lineedit_username)

        self.label_password = QLabel("Password:")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        self.v_layout.addWidget(self.label_password)
        self.v_layout.addWidget(self.lineedit_password)

        self.label_line_nr = QLabel("Line number:")
        self.lineedit_line_nr = QLineEdit()
        self.v_layout.addWidget(self.label_line_nr)
        self.v_layout.addWidget(self.lineedit_line_nr)

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login)
        self.v_layout.addWidget(self.button_login)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.v_layout)
        self.layout.addLayout(self.radio_layout)

        self.setLayout(self.layout)

    def login(self):
        self.username = self.lineedit_username.text()
        password = self.lineedit_password.text()
        self.line_nr = self.lineedit_line_nr.text()

        try:
            with open("fourth_project/credentials/credentials.txt", "r") as file:
                for line in file:
                    if f"log: {self.username} psswd: {password} line: {self.line_nr}" in line:
                        self.post_login_ui()
                        return
            QMessageBox.warning(
                self, "Error", "Invalid login credentials. Please try again.")
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Error", "Credentials file not found. Please make sure 'credentials.txt' exists.")

    def post_login_ui(self):
        # for i in reversed(range(self.layout.count())):
        #    self.layout.itemAt(i).widget().deleteLater()

        # set new UI
        self.label = QLabel("Logging was successful!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        QMessageBox.information(self, "Success", "Logging was accurate!")

        self.main = CustomMainWindow(
            self.username, self.line_nr, self.camera_on)
        self.main.show()
        self.close()

    def turn_camera_on(self):
        self.camera_on = True

    def turn_camera_off(self):
        self.camera_on = False
