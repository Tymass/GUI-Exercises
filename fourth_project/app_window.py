from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QHBoxLayout, QMessageBox, QLabel
from visualization import MainWindow
from engine import Engine
from PyQt5.QtCore import QThread, QTimer
from camera import CameraWindow
import matplotlib.pyplot as plt
from datetime import datetime


class EngineThread(QThread):
    def __init__(self, engine):
        QThread.__init__(self)
        self.engine = engine

    def run(self):
        self.engine.engineStart()


class CustomMainWindow(QMainWindow):
    def __init__(self, login, line, camera_on):
        super().__init__()

        self.setFixedSize(1400, 1000)
        self.login = login
        self.line = line
        self.camera_on = camera_on
        self.date = datetime.now()
        self.engine = Engine(name=self.line)

        self.timer = QTimer()
        self.timer.timeout.connect(self.userCheck)
        self.timer.start(30000)

        #self.camera = CameraWindow()
        self.widget1 = MainWindow(
            0, 'b-', 'fourth_project/logs/temp_log.txt', 'Temp [°C]')
        self.widget2 = MainWindow(
            0, 'r-', 'fourth_project/logs/shaft_log.txt', 'Shaft spin [Hz]')

        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.text_edit = QTextEdit(self)

        self.login_info = QLabel()
        self.login_info.setText(
            f'Logged as: {self.login} on line: {self.line}')
        self.logout_button = QPushButton("Logout", self)
        self.raport_button = QPushButton("Generate raport", self)

        self.login_layout = QHBoxLayout()
        self.login_layout.addWidget(self.login_info)
        self.login_layout.addWidget(self.logout_button)
        self.login_layout.addWidget(self.raport_button)

        self.setWindowTitle("Custom Real-Time Plot")
        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout(self.centralWidget())
        self.v_layout = QVBoxLayout()

        self.v_layout.addLayout(self.login_layout)
        self.v_layout.addWidget(self.widget1.canvas)
        self.v_layout.addWidget(self.widget2.canvas)
        self.v_layout.addWidget(self.start_button)
        self.v_layout.addWidget(self.stop_button)
        self.v_layout.addWidget(self.text_edit)

        self.layout.addLayout(self.v_layout)

        if self.camera_on == True:
            self.camera = CameraWindow()
            self.layout.addWidget(self.camera)

        self.start_button.clicked.connect(self.start_plot)
        self.stop_button.clicked.connect(self.stop_plot)
        self.logout_button.clicked.connect(self.checkResponse)
        self.raport_button.clicked.connect(self.generateRaport)

        self.info_box_timer = QTimer(self)
        self.info_box_timer.timeout.connect(self.update_info_box)
        self.info_box_timer.start(1000)

    def start_plot(self):
        self.thread = EngineThread(self.engine)
        if not self.thread.isRunning():
            self.engine.stop_cycle = False
            self.thread.start()
        self.widget1.timer.start()
        self.widget2.timer.start()

    def stop_plot(self):
        self.engine.stop_engine()
        self.widget1.timer.stop()
        self.widget2.timer.stop()

    def update_info_box(self):
        log_info = self.engine.log_info
        current_action = self.engine.current_action
        temperature = self.engine.enginge_temperature
        shaft_spin = self.engine.shaft_spin

        if log_info == "Engine overheated":
            log_info = '⚠️' + log_info
        elif log_info == "Critical temperature, emergency shutdown":
            log_info = '🚩' + log_info
        else:
            log_info = '🔨' + log_info

        self.text_edit.setPlainText(
            f"Log Info:                            {log_info}\nCurrent Action:                       {current_action} \nCurrent temperature:             {temperature} °C\nShaft spin:                              {shaft_spin} Hz")

    def userCheck(self):
        self.msg_box = QMessageBox(self)
        self.msg_box.setWindowTitle("User Check")
        self.msg_box.setText("Are you still there?")
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.show()

        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.checkResponse)
        self.check_timer.start(10000)  # 10 seconds in milliseconds

    def checkResponse(self):
        if self.msg_box.isVisible():
            self.check_timer.stop()
            self.timer.stop()
            self.msg_box.close()
            self.close()

    def generateRaport(self):
        with open('fourth_project/logs/temp_log.txt', 'r') as file:
            y_temp = [float(line.strip()) for line in file]

        with open('fourth_project/logs/shaft_log.txt', 'r') as file:
            y_shaft = [float(line.strip()) for line in file]

        x_temp = range(len(y_temp))
        x_shaft = range(len(y_shaft))

        plt.figure()
        plt.plot(x_temp, y_temp, label="Engine temperature")
        plt.plot(x_shaft, y_shaft, label="Shaft spin")
        plt.xlabel('Time [s]')
        plt.ylabel('Shaft spin [Hz] / Engine temperature [°C]')
        plt.grid()
        plt.legend()

        plt.savefig(
            'fourth_project/raports/' + f'{self.login}_{self.date.strftime("%d_%m_%H%M%S")}_raport.png')
