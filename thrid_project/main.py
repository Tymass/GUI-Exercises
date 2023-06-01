"Authored by Jakub Kłopotek Głowczewski"


from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
import sys
import random
import time
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Psychio Tests")
        self.setMinimumSize(500, 500)

        layout = QVBoxLayout()
        #stylesheet picked
        welcome_label = QLabel("Welcome to Psychio Tests!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 30pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
        """)
        #initializing varaibles to store from our tests
        self.color_times = None
        self.sound_times = None
        self.errors = None
        self.complex_times = None

        description_label = QLabel("Programs listed below will test your abilites \n and later evalute your results, and in the end we will receive the answer id \n you could become real life driver!")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            font-size: 20pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
        """)
        #adding buttons
        layout2 = QHBoxLayout()
        self.radio_red_green = QPushButton("Optical reaction test")
        self.radio_sounds = QPushButton("Hearing reaction test")
        self.radio_complex = QPushButton("Complex test")
        self.evalute = QPushButton("Evalute results!")
        
        # Style the buttons
        for btn in [self.radio_red_green, self.radio_sounds, self.radio_complex, self.evalute]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #abcdef;
                    font-size: 18pt;
                    color: #334455;
                    border: 2px solid #778899;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:pressed {
                    background-color: #778899;
                }
            """)

        layout.addWidget(welcome_label)
        layout.addWidget(description_label)
        layout2.addWidget(self.radio_red_green)
        layout2.addWidget(self.radio_sounds)
        layout2.addWidget(self.radio_complex)
        layout.addLayout(layout2)
        layout.addWidget(self.evalute)
        self.setLayout(layout)

        # Connect the button's clicked signal to the their functions
        self.radio_red_green.clicked.connect(self.open_green_and_red)
        self.green_and_red = None
        self.radio_sounds.clicked.connect(self.open_sounds)
        self.sounds = None
        self.radio_complex.clicked.connect(self.open_complex)
        self.complex=None

        self.evalute.clicked.connect(self.open_evaluation)
        self.evaluation=None
        #open window with tests functions
    def open_complex(self):
        if self.complex is None or not self.complex.isVisible():
            self.complex=Complex_test()
            self.complex.test_completed.connect(self.process_complex_results)
            self.complex.show()
    def process_complex_results(self, complex_times,errors):
        self.complex_times=complex_times
        self.errors=errors
        #print(complex_times,"errors:",errors)
    def open_green_and_red(self):
        # If green_and_red is None or not visible, create and show it
        if self.green_and_red is None or not self.green_and_red.isVisible():
            self.green_and_red = Green_and_Red()
            self.green_and_red.test_completed.connect(self.process_color_results)
            self.green_and_red.show()
    def process_color_results(self,color_times):
        self.color_times=color_times
        print(color_times)
    def open_sounds(self):
         if self.sounds is None or not self.sounds.isVisible():
            self.sounds= Sounds()
            self.sounds.test_completed.connect(self.process_sounds_results)
            self.sounds.show()
    def process_sounds_results(self, sound_times):
        self.sound_times=sound_times
        print(sound_times)
    def open_evaluation(self):
        if self.evaluation is None or not self.evaluation.isVisible():
            self.evaluation= Evaluate(self.color_times,self.sound_times,self.errors,self.complex_times)
            self.evaluation.show()
#class for evaluation
class Evaluate(QWidget):
    def __init__(self,process_color_results,sound_times,errors,complex_times):
        super().__init__()
        self.setWindowTitle("Evaluation")
        self.setMinimumSize(600,600)
        layout=QVBoxLayout()
        
        # Create the figure and plot
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)
        
        #calculate proportions and average values
        proportions,avg_clr,avg_snd,avg_cplx = self.calculate_proportions(process_color_results,sound_times,errors,complex_times)

        labels = ['optical reaction', 'sound reaction', 'awerness']
        ##Polar Graph code
        N = len(proportions)
        proportions = np.append(proportions, 1)
        theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
        x = np.append(np.sin(theta), 0)
        y = np.append(np.cos(theta), 0)
        triangles = [[N, i, (i + 1) % N] for i in range(N)]
        triang_backgr = tri.Triangulation(x, y, triangles)
        triang_foregr = tri.Triangulation(x * proportions, y * proportions, triangles)
        cmap = plt.cm.rainbow_r  
        colors = np.linspace(0, 1, N + 1)

        self._static_ax = static_canvas.figure.subplots()
        self._static_ax.tripcolor(triang_backgr, colors, cmap=cmap, shading='gouraud', alpha=0.4)
        self._static_ax.tripcolor(triang_foregr, colors, cmap=cmap, shading='gouraud', alpha=0.8)
        self._static_ax.triplot(triang_backgr, color='white', lw=2)
        for label, color, xi, yi in zip(labels, colors, x, y):
            self._static_ax.text(xi * 1.05, yi * 1.05, label,
                                ha='left' if xi > 0.1 else 'right' if xi < -0.1 else 'center',
                                va='bottom' if yi > 0.1 else 'top' if yi < -0.1 else 'center')
        self._static_ax.axis('off')
        self._static_ax.set_aspect('equal')
        
       ##

       ## Labels with results and some stylesheets
        label_style = """
            font-size: 20pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
        """

        color_label = QLabel(f"Average color reaction time: {avg_clr}")
        color_label.setAlignment(Qt.AlignCenter)
        color_label.setStyleSheet(label_style)
        layout.addWidget(color_label)

        sound_label = QLabel(f"Average sound reaction time: {avg_snd}")
        sound_label.setAlignment(Qt.AlignCenter)
        sound_label.setStyleSheet(label_style)
        layout.addWidget(sound_label)

        complex_label = QLabel(f"Average complex reaction time: {avg_cplx}")
        complex_label.setAlignment(Qt.AlignCenter)
        complex_label.setStyleSheet(label_style)
        layout.addWidget(complex_label)

        error_label = QLabel(f"Errors in complex test: {errors}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet(label_style)
        layout.addWidget(error_label)

        self.setLayout(layout)

        #simple normalization function for values from tests
    def calculate_proportions(self, process_color_results, sound_times, errors, complex_times):
        # Define maximum possible values
        max_time = 2.5  # Assuming 2.5 sec as the maximum potential time

        # Check if the user didn't play the game (None case), then set the normalized values to 0
        if process_color_results is None:
            norm_clr = 0
            avg_clr = 0  # Define default average in case of None
        else:
            avg_clr = sum(process_color_results) / len(process_color_results)
            norm_clr = 1 - (avg_clr / max_time)

        if sound_times is None:
            norm_snd = 0
            avg_snd = 0  # Define default average in case of None
        else:
            avg_snd = sum(sound_times) / len(sound_times)
            norm_snd = 1 - (avg_snd / max_time)

        if complex_times is None or errors == 0: # Also handle case when errors is 0 to prevent division by zero
            norm_cplx = 0
            avg_cplx = 0  # Define default average in case of None or errors being 0
        else:
            avg_cplx = (sum(complex_times) / len(complex_times)) / (errors+1)
            norm_cplx = 1 - (avg_cplx / max_time)

        return [norm_clr, norm_snd, norm_cplx], avg_clr, avg_snd, avg_cplx



#class complex test
class Complex_test(QWidget):
    #Signal to send to Main Class when test is over
    test_completed=Signal(list,int)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Complex test")
        self.setMinimumSize(500,500)

        self.layout = QVBoxLayout() 

        description_label = QLabel("The screen will change color and play a sound simultaneously at random intervals. \n When you hear a high pitched sound while the screen is green or a low pitched sound when the \nscreen is red, press the button as quickly as possible.")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            font-size: 18pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
        """)
        self.start_button = QPushButton("Start")
        self.test_button = QPushButton("Test")
        self.reaction_button = QPushButton()

        for btn in [self.start_button, self.test_button, self.reaction_button]:
            btn.setStyleSheet("""
            QPushButton {
            background-color: #abcdef;
             font-size: 18pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            }
            QPushButton:pressed {
            background-color: #778899;
            }
            """)
        self.reaction_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reaction_button.setEnabled(False)

        
        self.layout.addWidget(description_label)
        self.layout.addWidget(self.test_button)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.reaction_button)
        self.setLayout(self.layout)

        #counter of wrong answers
        self.wrong_option=0

        self.timer = QTimer()
        self.timer.timeout.connect(self.play_sound_and_change_color)
        self.timer2=QTimer()
        self.timer2.timeout.connect(self.timer_timeout)
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.sounds = {"high": "sound_effects/high_pitch.wav", "low": "sound_effects/low_pitch.wav"}
        
        self.colors = {"high": "green", "low": "red"}
        self.sound_combination = None
        self.start_time = 0
        self.end_time = 0
        self.complex_reaction_times=[]
        self.test_mode=False
        
        self.start_button.clicked.connect(self.start_game)
        self.test_button.clicked.connect(self.test_modefun)
        self.reaction_button.clicked.connect(self.check_reaction)
        self.timeout=False
        #timer timeout for in between games
    def timer_timeout(self):
        self.timeout=True
        self.player.stop()
        self.reaction_button.setStyleSheet(f"background-color: white")
        self.timer2.stop()
        self.check_reaction()
        #play music and initialize game after timer runs out
    def play_sound_and_change_color(self):
        self.timer.stop()   
        #second timer to stop if combinations do not match
        self.timer2.start(5000)
        self.start_time=time.time()
        self.sound_combination = random.choice(list(self.sounds.keys()))
        self.player.setSource(QUrl.fromLocalFile(self.sounds[self.sound_combination]))
        self.color_combination=random.choice(list(self.colors.keys()))
        self.reaction_button.setStyleSheet(f"background-color: {self.colors[self.color_combination]}")
        self.reaction_button.setEnabled(True)
        self.player.play()
        self.start_time=time.time()
    #starting game
    def start_game(self):
        self.reaction_button.setStyleSheet("background-color: white")
        self.timer.start(random.randint(2000, 5000))
    #for test mode
    def test_modefun(self):
        self.complex_reaction_times=[]
        self.test_mode=True
        self.start_game()
    #evaluate user answers
    def check_reaction(self):
        if self.sound_combination==self.color_combination and self.timeout==False:
            self.player.stop()
            self.end_time=time.time()
            self.timer2.stop()
            print("you are correct!")
            print("reaction time saved!")
            self.complex_reaction_times.append(self.end_time-self.start_time)
        elif self.sound_combination!=self.color_combination and self.timeout==False:
            self.player.stop()
            self.end_time=time.time()
            self.timer2.stop()
            print("you are incorrect!")
            self.wrong_option+=1
        elif self.timeout==True and self.sound_combination!=self.color_combination:
            print("you are right! Combinations do not match!")
            self.timeout=False
        elif self.timeout==True and self.sound_combination==self.color_combination:
            print("Wrong! Sound and color do match!")
            self.wrong_option+=1
            self.timeout=False
        if len(self.complex_reaction_times)<3:
            self.start_game()
        elif len(self.complex_reaction_times)==3 and self.test_mode==False:   #if len is enoguh then we stop the loop
            print("All tests completed, please refer to main page!")
            self.test_completed.emit(self.complex_reaction_times,self.wrong_option)
            self.reaction_button.setEnabled(False)
            self.reaction_button.setStyleSheet("background-color: black")
        elif len(self.complex_reaction_times)==3 and self.test_mode==True:
            print("Prepartaion completed! Now apporach test!")
            self.test_mode=False
            self.complex_reaction_times=[]
            self.reaction_button.setEnabled(False)
# sounds class for test
class Sounds(QWidget):
    test_completed = Signal(list)  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hearing reaction test")
        self.setMinimumSize(500,500)
        description_label = QLabel("The music will start to play in random time with incresing volume,\n when you hear it you press the button\n You can check the game running test, it will not save your  results!\n Preparation consist of one music sample that is diffrent then testing samples ")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            font-size: 18pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
        """)
        self.layout = QVBoxLayout() 
        self.start_button=QPushButton("Start")
        self.test_button=QPushButton("Test")
        self.reaction_button = QPushButton("I can hear!")

        for btn in [self.start_button, self.test_button, self.reaction_button]:
            btn.setStyleSheet("""
             QPushButton {
            background-color: #abcdef;
            font-size: 18pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
                }
            QPushButton:pressed {
            background-color: #778899;
            }
            """)
        self.layout.addWidget(description_label)
        self.layout.addWidget(self.test_button)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.reaction_button)
        self.setLayout(self.layout)

        self.songs = ["sound_effects/test.wav", "sound_effects/piano.wav", "sound_effects/top.wav"]
        self.volume_increase_timer=QTimer()
        self.volume_increase_timer.timeout.connect(self.increase_volume)
        self.player=QMediaPlayer()
        self.test_mode=False
        self.start_time=0
        self.end_time=0

        self.timer=QTimer()

        self.timer.timeout.connect(self.play_music)
        self.reaction_times_sound=[]
        self.start_button.clicked.connect(self.start_game)
        self.test_button.clicked.connect(self.test_start)
        self.reaction_button.clicked.connect(self.stop_music)
    def test_start(self):
        self.reaction_times_sound=[]
        self.test_mode=True
        self.start_game()
    def start_game(self):
        self.timer.start(random.randint(2000, 5000))  # waits between 2 and 5 seconds
    def play_music(self):
        self.timer.stop()
        self.start_time=time.time()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        if self.test_mode:
            self.player.setSource(QUrl.fromLocalFile("sound_effects/ambulance.wav"))
        else:
            
            song_to_play = random.choice(self.songs)
           # print("playing:",song_to_play)
            self.player.setSource(QUrl.fromLocalFile(song_to_play))
            self.songs.remove(song_to_play)
        self.audioOutput.setVolume(0)  # start with volume 0
        self.player.play()
      #  print("starting")
        self.volume_increase_timer.start(100)  # increase volume every 1 second

    def increase_volume(self):
        current_volume = self.audioOutput.volume()
        if current_volume < 1:  # 100 is the max volume
          #  print("inncresed volume")
            self.audioOutput.setVolume(current_volume + 0.01)  # increase volume by 1
        else:
            self.volume_increase_timer.stop()  # stop increasing volume once it reaches max
    def stop_music(self):
        if self.player.isPlaying():
            self.end_time = time.time()
            self.player.stop()
            self.volume_increase_timer.stop() 
            if self.test_mode:
                print("Reaction Time:", self.end_time - self.start_time, "seconds")
                self.reaction_times_sound.append(self.end_time - self.start_time)
            else: 
                self.reaction_times_sound.append(self.end_time - self.start_time)
                print("Reaction time saved!")
            
            if len(self.reaction_times_sound) == 1 and self.test_mode:
                print("Completed preparation, now you can approach real test!")
                self.reaction_times_sound=[]
                self.test_mode=False
            elif len(self.reaction_times_sound)==3: 
                print("All tests completed please refer to main window")
                self.test_completed.emit(self.reaction_times_sound) 
                
            elif len(self.reaction_times_sound)<3 and not self.test_mode:
                self.start_game()
        else:
            print("Music haven't started, don't cheat!")
            self.reaction_times_sound=[]
            self.timer.stop()

class Green_and_Red(QWidget):
    test_completed = Signal(list)  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optical Reaction Test")
        self.setMinimumSize(500, 500)
        
        self.reaction_times=[]
        self.layout = QVBoxLayout() 
        
        description_label = QLabel("Simply press the start button, the background should \n  change color to red,and then when it turn green \n press the button as fast as possible.\n Test button lets you play without saving results,\n feel free to check yourself!")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            font-size: 18pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
        """)


        self.start_button = QPushButton("Start")
        self.test_button=QPushButton("Test")
        self.reaction_button = QPushButton()
        self.reaction_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reaction_button.setEnabled(False)
        for btn in [self.start_button, self.test_button, self.reaction_button]:
            btn.setStyleSheet("""
            QPushButton {
            background-color: #abcdef;
            font-size: 18pt;
            color: #334455;
            border: 2px solid #778899;
            border-radius: 10px;
            padding: 10px;
             }
             QPushButton:pressed {
            background-color: #778899;
         }
        """)

        self.layout.addWidget(description_label)
        self.layout.addWidget(self.test_button)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.reaction_button)
        self.setLayout(self.layout)
        self.test_mode=False
        self.start_time = 0
        self.end_time = 0
        self.done=0
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_to_green)
        self.test_button.clicked.connect(self.test_modefun)
        self.start_button.clicked.connect(self.start_game)
        self.reaction_button.clicked.connect(self.stop_game)
    def test_modefun(self):
        self.reaction_times=[]
        self.test_mode=True
        self.start_game()
    def start_game(self):
            
            self.reaction_button.setStyleSheet("background-color: red")
            self.reaction_button.setEnabled(True)
            self.timer.start(random.randint(2000, 5000))  # waits between 2 and 5 seconds

    def change_to_green(self):
        self.timer.stop()
        self.start_time = time.time()
        self.reaction_button.setStyleSheet("background-color: green")

    def stop_game(self):
        if self.reaction_button.styleSheet() == "background-color: green":
            self.end_time = time.time()
            if self.test_mode:
                print("Reaction Time:", self.end_time - self.start_time, "seconds")
                self.reaction_times.append(self.end_time - self.start_time)
            else: 
                self.reaction_times.append(self.end_time - self.start_time)
                print("Reaction time saved!")
            
            if len(self.reaction_times) == 5:
                if self.test_mode:
                    print("Completed preparation, now you can approach real test!")
                    self.reaction_times=[]
                    self.test_mode=False
                else: 
                    print("All tests completed please refer to main window")
                    self.test_completed.emit(self.reaction_times) 
                self.reaction_button.setEnabled(False)
                
            elif len(self.reaction_times)!=5 or self.test_mode:
                self.start_game()
        elif self.reaction_button.styleSheet()=="background-color: red":
            print("Failed!,Don't cheat")
            self.reaction_times=[]
            self.reaction_button.setEnabled(False)
            self.timer.stop()
            self.reaction_button.setStyleSheet("background-color: yellow")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
