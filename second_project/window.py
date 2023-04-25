from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Text Display Example')

        # Create the text input widget
        self.text_input = QTextEdit(self)

        # Create the search bar and connect to the search function
        self.search_bar = QAction('Search Files', self)
        self.search_bar.triggered.connect(self.search_files)

        # Add the search bar to the menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.search_bar)

        # Create a separate window to display the text
        self.text_display_window = QWidget()
        self.text_display_window.setWindowTitle('Text Display')
        self.text_display_window.setGeometry(100, 100, 800, 600)

        # Create a label to display the text in the new window
        self.text_display_label = QLabel(self.text_display_window)
        layout = QVBoxLayout(self.text_display_window)
        layout.addWidget(self.text_display_label)

        # Set the central widget and layout
        self.setCentralWidget(self.text_input)
        self.setGeometry(100, 100, 800, 600)

    def search_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Text File', '', 'Text Files (*.txt);;All Files (*)', options=options)

        if file_name:
            with open(file_name, 'r') as file:
                file_content = file.read()
                self.text_input.setPlainText(file_content)
                self.text_display_label.setText(file_content)
                self.text_display_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
