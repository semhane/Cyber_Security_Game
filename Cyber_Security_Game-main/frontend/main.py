# frontend/main.pyimport sys
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QSizePolicy, QStackedWidget
from backend.supabase_client import supabase

# Import your challenges
from games.password_strength.challenge_one import PasswordStrengthChallenge
from games.phishing_quiz.challenge_one import PhishingEmailChallenge_one
from games.phishing_quiz.challenge_two import PhishingEmailChallenge_two
from games.phishing_quiz.challenge_three import PhishingEmailChallenge_three  # Add this import

class CyberDefendApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberDefend - Security Challenges")
        self.setFixedSize(1000, 700)
        self._set_dark_theme()
        
        # Initialize score
        self.total_score = 0
        
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create challenges
        self.password_challenge = PasswordStrengthChallenge()
        self.phishing_challenge_1 = PhishingEmailChallenge_one()
        self.phishing_challenge_2 = PhishingEmailChallenge_two()
        self.phishing_challenge_3 = PhishingEmailChallenge_three()  # Add Challenge 3
        
        # Add to stack
        self.stacked_widget.addWidget(self.password_challenge)
        self.stacked_widget.addWidget(self.phishing_challenge_1)
        self.stacked_widget.addWidget(self.phishing_challenge_2)
        self.stacked_widget.addWidget(self.phishing_challenge_3)  # Add Challenge 3 to stack
        
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Connect signals
        self.password_challenge.challenge_complete.connect(self.show_phishing_challenge_1)
        self.phishing_challenge_1.challenge_complete.connect(self.show_phishing_challenge_2)
        self.phishing_challenge_2.challenge_complete.connect(self.show_phishing_challenge_3)  # Connect Challenge 2 to 3
        self.phishing_challenge_3.challenge_complete.connect(self.all_challenges_complete)  # Connect Challenge 3 completion
    
    def show_phishing_challenge_1(self, earned_score):
        """Switch to the first phishing challenge and update score"""
        self.total_score += earned_score
        self.phishing_challenge_1.score = self.total_score
        self.stacked_widget.setCurrentWidget(self.phishing_challenge_1)

    def show_phishing_challenge_2(self, earned_score):
        """Switch to the second phishing challenge and update score"""
        self.total_score += earned_score
        self.phishing_challenge_2.score = self.total_score
        self.stacked_widget.setCurrentWidget(self.phishing_challenge_2)
        
    def show_phishing_challenge_3(self, earned_score):
        """Switch to the third phishing challenge and update score"""
        self.total_score += earned_score
        self.phishing_challenge_3.score = self.total_score
        self.phishing_challenge_3.level = "03"  # Update level number
        self.stacked_widget.setCurrentWidget(self.phishing_challenge_3)
        
    def all_challenges_complete(self, earned_score):
        """Handle completion of all challenges"""
        self.total_score += earned_score
        # Show completion message with final score
        QMessageBox.information(self, "Congratulations!", 
                               f"All challenges completed!\nFinal Score: {self.total_score}")
        # You could add a "Restart" button here if you want

    def _set_dark_theme(self):
        """Apply dark theme to the application"""
        dark_palette = QPalette()
        
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.Base, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.Text, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.Button, QColor(70, 70, 70))
        dark_palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #00ff00;
            }
            QStackedWidget {
                background-color: #1e1e1e;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberDefendApp()
    window.show()

    print("Testing Supabase connection...", flush=True)

    try:
        response = supabase.table("users").select("*").limit(1).execute()

        # Check if there was an error in the response
        if response.error:
            print(f"Error: {response.error}")
        else:
            print("Supabase connection successful! Got response:", response.data)
    except Exception as e:
        print("Supabase connection FAILED:", e)


    sys.exit(app.exec_())
