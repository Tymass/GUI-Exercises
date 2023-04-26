from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os


def text_to_serial_string(text):
    start_bit = '0'
    stop_bits = '11'
    serial_string = ""

    for char in text:
        # Convert to 8-bit binary and reverse the order (LSB to MSB)
        char_bits = format(ord(char), '08b')[::-1]
        serial_char = start_bit + char_bits + stop_bits
        serial_string += serial_char

    return serial_string


def serial_string_to_text(serial_string):
    start_bit = '0'
    stop_bits = '11'

    text = ""
    index = 0
    while index < len(serial_string):
        if serial_string[index] == start_bit:  # Check for start bit
            # Extract character bits (still reversed)
            char_bits_reversed = serial_string[index + 1:index + 9]
            # Reverse the order back to the original (MSB to LSB)
            char_bits = char_bits_reversed[::-1]
            char = chr(int(char_bits, 2))  # Convert binary to ASCII character
            text += char
            # Move to the next character (1 start bit + 8 character bits + 2 stop bits)
            index += 11
        else:
            raise ValueError("Invalid bit stream format")

    return text


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.file_lines = []  # Initialize an empty list for file content
        self.working_directory = os.getcwd() + "/second_project/dictionaries"

    def initUI(self):
        self.setWindowTitle('PyQt5 Simple GUI Example')

        # Create the text input widget with info label
        self.text_input = QTextEdit(self)
        self.text_input_info = QLabel(self)
        self.text_input_info.setText("Enter your text")

        # Create the display boxes with info labels
        self.display_box1 = QTextEdit(self)
        self.display_box1.setReadOnly(True)
        self.display_box2 = QTextEdit(self)
        self.display_box2.setReadOnly(True)
        self.display_box3 = QTextEdit(self)
        self.display_box3.setReadOnly(True)

        self.display_box1_info = QLabel(self)
        self.display_box1_info.setText("Reversed ASCII characters (as bits)")
        self.display_box2_info = QLabel(self)
        self.display_box2_info.setText("Forbidden words dictionary")
        self.display_box3_info = QLabel(self)
        self.display_box3_info.setText("Your proper text")

        # Create the QPushButton widgets
        self.button1 = QPushButton('Show binary code', self)
        self.button1.clicked.connect(self.update_box1)

        self.button2 = QPushButton('Show censored code', self)
        self.button2.clicked.connect(self.update_box2)

        # Create the main layout
        main_layout = QVBoxLayout()

        # Add the text input widget to the layout
        main_layout.addWidget(self.text_input_info)
        main_layout.addWidget(self.text_input)
        main_layout.addWidget(self.display_box3_info)
        main_layout.addWidget(self.display_box2)

        # Create a QHBoxLayout for the display labels
        labels_info_layout = QHBoxLayout()
        labels_info_layout.addWidget(self.display_box1_info)
        labels_info_layout.addWidget(self.display_box2_info)

        # Create a QHBoxLayout for the display boxes
        display_boxes_layout = QHBoxLayout()
        display_boxes_layout.addWidget(self.display_box1)
        display_boxes_layout.addWidget(self.display_box3)

        # Add the QHBoxLayout to the main layout
        main_layout.addLayout(labels_info_layout)
        main_layout.addLayout(display_boxes_layout)

        # Add the QPushButton widgets to the main layout
        main_layout.addWidget(self.button1)
        main_layout.addWidget(self.button2)

        # Create a central widget for the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create the menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        # Create the open file action
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

    def update_box1(self):
        text = self.text_input.toPlainText()
        # text.lower()
        self.text_bit = text_to_serial_string(text)
        #censored_text = self.censor_text(text)
        self.display_box1.setPlainText(self.text_bit)

    def update_box2(self):
        try:
            text = self.text_input.toPlainText()
            censored_text = self.censor_text(text.lower())
            self.display_box2.setPlainText(censored_text)
        except AttributeError:  # Handle empty dictionary
            QMessageBox.warning(self, "Error", "Choose directory first")
            return

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Open Text File', f'{self.working_directory}', 'Text Files (*.txt);;All Files (*)', options=options)

        if file_name:
            with open(file_name, 'r') as file:
                self.file_lines = file.readlines()
                encoded_lines = [text_to_serial_string(
                    line) for line in self.file_lines]
                self.encoded_file_content = ''.join(encoded_lines)
                file_content = ''.join(self.file_lines)
                self.display_box3.setPlainText(file_content)

    def censor_text(self, input_text):
        encoded_input_text = text_to_serial_string(input_text)
        words_to_censor = serial_string_to_text(
            self.encoded_file_content).split()

        for word in words_to_censor:
            encoded_word = text_to_serial_string(word)
            if encoded_word in encoded_input_text:
                censor_string = '*' * len(word)
                input_text = input_text.replace(word, censor_string)

        return input_text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    simple_gui = MainWindow()
    simple_gui.show()
    sys.exit(app.exec_())
