#Rock Paper Scissor

import sys, os, random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.text_label = QLabel("Press anything to start..", self)
        self.comp_choice_screen = QLabel("", self)
        self.player_choice_screen = QLabel("", self)
        self.rock = QPushButton("🗿", self)
        self.paper = QPushButton("📃", self)
        self.scissor = QPushButton("✂", self)

        self.started = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle("ROCK-PAPER-SCISSOR")
        icon_path = os.path.join(os.path.dirname(__file__), "assets/Icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(self.width(), 400)

        self.comp_choice_screen.setAlignment(Qt.AlignCenter)
        self.player_choice_screen.setAlignment(Qt.AlignCenter)
        self.text_label.setAlignment(Qt.AlignCenter)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.rock)
        hbox.addWidget(self.paper)
        hbox.addWidget(self.scissor)

        main_screen = QHBoxLayout()
        main_screen.addWidget(self.comp_choice_screen)
        main_screen.addWidget(self.player_choice_screen)

        vbox = QVBoxLayout()
        vbox.addWidget(self.text_label)
        vbox.addLayout(main_screen)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.text_label.setObjectName("text_label")
        self.comp_choice_screen.setObjectName("comp_choice_screen")
        self.player_choice_screen.setObjectName("player_choice_screen")

        self.setStyleSheet("""
        QPushButton, QLabel{
            padding: 5px;
            font-family: Segoe UI Emoji;   
            background-color: gray;                        
        }
        QPushButton{
            font-size: 50px;
            border: 2px solid black;
            border-radius: 2px;           
        }
        QPushButton:hover{
            background-color: hsl(0, 0, 88);                 
        }
        QPushButton:disabled{
            background-color: #aaa;
            border: 2px solid #888;                   
        }
        QLabel{
            border: 2px solid #0078D7;
            border-radius: 5px;
            padding: 6px 12px;                   
        }
        QLabel#comp_choice_screen, player_choice_screen{
            font-size: 140px;
        }
        QLabel#text_label{
            font-size: 50px;
            font-family: Arial;                   
        }
    """)
        
        self.rock.clicked.connect(lambda: self.play("🗿"))
        self.paper.clicked.connect(lambda: self.play("📃"))
        self.scissor.clicked.connect(lambda: self.play("✂"))

    def play(self, player_choice):
        self.comp_choice_screen.setText("")

        if not self.started:
            self.started = True
            self.text_label.setText("Choose something")
            return
        
        #Temporarily disable all button
        self.rock.setEnabled(False)
        self.paper.setEnabled(False)
        self.scissor.setEnabled(False)

        self.step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(800)
        
        self.comp_choice = random.choice(["🗿", "📃", "✂"])
        self.result = self.get_result(player_choice, self.comp_choice)
        self.player_choice_screen.setText(player_choice)
        self.player_choice_screen.setStyleSheet("font-size: 140px")

    def loading(self):
        self.step += 1
        match self.step:
            case 1:
                self.text_label.setText(".")
            case 2:
                self.text_label.setText("..")
            case 3:
                self.text_label.setText("...")
            case 4:
                self.text_label.setText(self.result)
                self.comp_choice_screen.setText(self.comp_choice)
                self.timer.stop()
                self.step = 0   
                self.timer.start(1300)
                self.timer.timeout.connect(self.play_again)
    
    def get_result(self, player, comp):
        if player == comp:
            return "Draw"
        elif (player == "🗿" and comp == "✂") or \
             (player == "📃" and comp == "🗿") or \
             (player == "✂" and comp == "📃"):
              
            return "You win🤩"
        else:
            return "You lose😭"
        
    def play_again(self):
        self.text_label.setText("Play again?")
        #self.comp_choice_screen.setText("")
        #self.player_choice_screen.setText("")

        self.rock.setEnabled(True)
        self.paper.setEnabled(True)
        self.scissor.setEnabled(True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
