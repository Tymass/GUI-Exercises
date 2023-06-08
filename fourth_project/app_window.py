import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QHBoxLayout
# the name of your visualization module
from visualization import MainWindow
from engine import Engine  # the name of your engine module
from PyQt5.QtCore import QThread, QTimer
from camera import CameraWindow


class EngineThread(QThread):
    def __init__(self, engine):
        QThread.__init__(self)
        self.engine = engine

    def run(self):
        self.engine.engineStart()


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1900, 1000)

        # Create an engine
        self.engine = Engine(name="1")

        #self.camera = CameraWindow()
        # Create a Matplotlib figure and canvas
        self.widget1 = MainWindow(0, 'b-')
        self.widget2 = MainWindow(0, 'r-')

        # Create two buttons and QTextEdit
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.text_edit = QTextEdit(self)

        # Set up the main window
        self.setWindowTitle("Custom Real-Time Plot")
        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout(self.centralWidget())
        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.widget1.canvas)
        self.v_layout.addWidget(self.widget2.canvas)
        self.v_layout.addWidget(self.start_button)
        self.v_layout.addWidget(self.stop_button)
        self.v_layout.addWidget(self.text_edit)

        self.layout.addLayout(self.v_layout)
        # self.layout.addWidget(self.camera)

        # Connect button signals to their respective slots
        self.start_button.clicked.connect(self.start_plot)
        self.stop_button.clicked.connect(self.stop_plot)

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

        if log_info == "Engine overheated":
            log_info = '⚠️' + log_info
        elif log_info == "Critical temperature, emergency shutdown":
            log_info = '🚩' + log_info
        else:
            log_info = '🔨' + log_info

        self.text_edit.setPlainText(
            f"Log Info:                            {log_info}\nCurrent Action:                       {current_action} \nCurrent temperature:             {temperature} °C")
