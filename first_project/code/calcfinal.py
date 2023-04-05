from PySide6.QtWidgets import *
import sys
from calculator3_ui import Ui_Form
from PySide6.QtCore import QFile
from PySide6.QtGui import *
from PySide6.QtCore import *

class CombinedWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.style_sheet=True
        # Create instances of Calculator and Clock
        self.clock = Clock()
        self.calculator = Calculator()
        # Set up the layout
        layout = QHBoxLayout()
        layout.addWidget(self.calculator)
        layout.addWidget(self.clock)

        self.calculator.ui.change_clock.clicked.connect(self.clock.toggle)
        self.calculator.ui.change_stylesheet.clicked.connect(self.toggle_styles)
        self.setLayout(layout)


    def toggle_styles(self):
        self.style_sheet=not self.style_sheet
        self.changestyles()
    def changestyles(self):
        if self.style_sheet:
            self.setStyleSheet("background-color:blue")
            self.calculator.setStyleSheet("""
                QPushButton{background-color:yellow}
                QPushButton{font:bold}
                QPlainTextEdit{background-color:lightgray}
                QPlainTextEdit{color:black}
                QPlainTextEdit{font:bold}
            """)
            self.clock.change_colors(Qt.green, Qt.red, Qt.white)  # Added digital clock font color
        else:
            self.setStyleSheet("background-color:cyan")
            self.calculator.setStyleSheet("""
                QPushButton{background-color:green}
                QPushButton{font:italic}
                QPlainTextEdit{background-color:lightyellow}
                QPlainTextEdit{color:blue}
                QPlainTextEdit{font:italic}
            """)
            self.clock.change_colors(Qt.darkBlue, Qt.darkMagenta, Qt.black)  # Added digital clock font color
        # Set the layout for this widget
        
        

class Calculator(QWidget):
    def __init__(self):
        super(Calculator,self).__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.stack=[]
        self.result=0
        self.ui.button_0.clicked.connect(lambda: self.onButtonClicked("0")) 
        self.ui.button_1.clicked.connect(lambda: self.onButtonClicked("1"))  
        self.ui.button_2.clicked.connect(lambda: self.onButtonClicked("2"))  
        self.ui.button_3.clicked.connect(lambda: self.onButtonClicked("3"))  
        self.ui.button_4.clicked.connect(lambda: self.onButtonClicked("4"))  
        self.ui.button_5.clicked.connect(lambda: self.onButtonClicked("5"))  
        self.ui.button_6.clicked.connect(lambda: self.onButtonClicked("6"))  
        self.ui.button_7.clicked.connect(lambda: self.onButtonClicked("7"))  
        self.ui.button_8.clicked.connect(lambda: self.onButtonClicked("8"))  
        self.ui.button_9.clicked.connect(lambda: self.onButtonClicked("9"))  
        self.ui.button_clr.clicked.connect(lambda: self.clear())  
        self.ui.button_back.clicked.connect(self.erase)
        self.ui.button_coma.clicked.connect(lambda: self.onButtonClicked("."))
        self.ui.button_mno.clicked.connect(lambda: self.onButtonClicked("*"))
        self.ui.button_div.clicked.connect(lambda: self.onButtonClicked("/"))
        self.ui.button_plus.clicked.connect(lambda: self.onButtonClicked("+"))
        self.ui.button_minus.clicked.connect(lambda: self.onButtonClicked("-"))
        #self.ui.change_clock.clicked.connect(clock.toggle)
        self.ui.buttonequal.clicked.connect(self.equal)
        self.ui.plainTextEdit.setReadOnly(True)
      

    def onButtonClicked(self,number):  
        self.stack.append(number)
        text = "".join(str(n) for n in self.stack)
        self.updatetext(text)
    def updatetext(self,text):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.appendPlainText(text)
    def erase(self):
        self.stack.pop()
        text = "".join(str(n) for n in self.stack)
        self.updatetext(text)
    def clear(self):
        self.ui.plainTextEdit.clear()
        self.stack.clear()
    def equal(self):  
        expression = "".join(self.stack)
        self.result = eval(expression)
        self.updatetext(str(self.result))
class Clock(QWidget):
    def __init__(self):
        super().__init__()
        self.is_analog=True
        # creating a timer object
        timer = QTimer(self)
        self.clock_style = Qt.white
        timer.timeout.connect(self.update)
  
        timer.start(1000)
        self.initializeclock()

    def change_colors(self, b_color, s_color, clock_font_color):
        self.bColor = b_color
        self.sColor = s_color
        self.clock_style = clock_font_color  # Update the digital clock font color
        self.update()

    def toggle(self):
        self.is_analog=not self.is_analog
        self.update()
    def initializeclock(self):
        self.hPointer = QPolygon([QPoint(6, 7),
                                        QPoint(-6, 7),
                                        QPoint(0, -50)])
  
        # creating minute hand
        self.mPointer = QPolygon([QPoint(6, 7),
                                  QPoint(-6, 7),
                                  QPoint(0, -70)])
  
        # creating second hand
        self.sPointer = QPolygon([QPoint(1, 1),
                                  QPoint(-1, 1),
                                  QPoint(0, -90)])
        # colors
        # color for minute and hour hand
        self.bColor = Qt.green
  
        # color for second hand
        self.sColor = Qt.red
    

    def draw_digital_clock(self, event):
        painter = QPainter(self)
        current_time = QTime.currentTime()
        time_text = current_time.toString('hh:mm:ss')
        font = QFont('Arial', 20, QFont.Bold)
        painter.setFont(font)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.clock_style)  # Set the font color using clock_style
        painter.drawText(event.rect(), Qt.AlignCenter, time_text)
    def draw_analog_clock(self,event):
        # getting minimum of width and height
        # so that clock remain square
        rec = min(self.width(), self.height())
  
        # getting current time
        tik = QTime.currentTime()
  
        # creating a painter object
        painter = QPainter(self)
  
  
        # method to draw the hands
        # argument : color rotation and which hand should be pointed
        def drawPointer(color, rotation, pointer):
  
            # setting brush
            painter.setBrush(QBrush(color))
  
            # saving painter
            painter.save()
  
            # rotating painter
            painter.rotate(rotation)
  
            # draw the polygon i.e hand
            painter.drawConvexPolygon(pointer)
  
            # restore the painter
            painter.restore()
  
  
        # tune up painter
        painter.setRenderHint(QPainter.Antialiasing)
  
        # translating the painter
        painter.translate(self.width() / 2, self.height() / 2)
  
        # scale the painter
        painter.scale(rec / 200, rec / 200)
  
        # set current pen as no pen
        painter.setPen(Qt.NoPen)
  
  
        # draw each hand
        drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer)
        drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer)
        drawPointer(self.sColor, (6 * tik.second()), self.sPointer)
  
  
        # drawing background
        painter.setPen(QPen(self.bColor))
  
        # for loop
        for i in range(0, 60):
  
            # drawing background lines
            if (i % 5) == 0:
                painter.drawLine(87, 0, 97, 0)
  
            # rotating the painter
            painter.rotate(6)
  
        # ending the painter
        painter.end()

    def paintEvent(self, event):
        if self.is_analog:
            self.draw_analog_clock(event)
        else:
            self.draw_digital_clock(event)

        
        
if __name__ == '__main__':
    app = QApplication([])
    combined_widget = CombinedWidget()
    combined_widget.resize(1000, 500)
    combined_widget.show()
    combined_widget.show()
    app.exec()
