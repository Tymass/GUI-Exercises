import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, shared_dict):
        super().__init__()

        #self.signal = signal
        # Create a Matplotlib figure and canvas
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.shared_dict = shared_dict

        # Set up the main window
        self.setWindowTitle("Real-Time Plot")
        self.setCentralWidget(QWidget(self))
        self.layout = QVBoxLayout(self.centralWidget())
        self.layout.addWidget(self.canvas)

        # Initialize the plot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 500)
        self.ax.grid()
        # self.setGrid(True)

        # Generate the line data
        self.x = []
        self.y = []

        self.line, = self.ax.plot([], [], 'b-')

        # Start the real-time plot
        self.index = 0
        self.timer = self.canvas.new_timer(
            interval=100)  # Update every 100 milliseconds

        self.timer.add_callback(self.update_plot)
        self.timer.start()
        # if self.signal == 1:
        #    self.timer.stop()
        if self.shared_dict['engine_mode'] == 1:
            self.timer.stop()

    def update_plot(self):
        # Read the last line from the file
        try:
            with open("engine_data.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    self.y.append(float(last_line.strip()))

                    # Dynamically update the x-axis data
                    self.x.append(self.x[-1] + 1 if self.x else 0)
                else:
                    # No more data, stop the timer
                    self.timer.stop()

        except FileNotFoundError:
            pass  # handle file not found error here

        # Update the line plot
        if self.y:
            self.line.set_data(self.x, self.y)
            # Update the x-axis limit
            if self.x[-1] > 200:
                self.ax.set_xlim(self.x[-1] - 200, self.x[-1])
            else:
                self.ax.set_xlim(0, self.x[-1])

            self.canvas.draw()


# if __name__ == "__main__":
#    app = QApplication(sys.argv)

#    window = MainWindow()
#    window.show()

#    sys.exit(app.exec_())
