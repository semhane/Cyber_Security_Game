# frontend/games/password_strength_challenge.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QFrame, QLineEdit, QProgressBar, QPushButton)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
import re

from ..phishing_quiz.challenge_one import PhishingEmailChallenge
from PyQt5.QtWidgets import (QWidget, QSizePolicy)  # Make sure QSizePolicy is imported

from PyQt5.QtWidgets import QStackedWidget  # Add this
from PyQt5.QtCore import pyqtSignal 
    
class PasswordStrengthChallenge(QMainWindow):

    challenge_complete = pyqtSignal(int)  # Will send the earned score


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CyberDefend - Password Security Challenge")
        self.setFixedSize(1000, 700)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set dark theme palette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))
        self.setPalette(palette)
        
        self.score = 170  # Starting score
        
        # Create the custom title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #282828;")  # 👈 Add this line
        title_bar_layout = QHBoxLayout()
        title_bar.setLayout(title_bar_layout)

        
        # Add the three colored dots on the left
        dots_container = QWidget()
        dots_layout = QHBoxLayout(dots_container)
        dots_layout.setSpacing(8)
        dots_layout.setContentsMargins(15, 0, 0, 0)  # Left margin only
        
        for color in ["#FF5F56", "#FFBD2E", "#27C93F"]:  # Red, Yellow, Green
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            dots_layout.addWidget(dot)
        
        title_bar_layout.addWidget(dots_container)
        
        # Add the centered title
        title_label = QLabel("CYBERDEFEND PROTOCOL v2.7.1")
        title_label.setFont(QFont("Consolas", 10, QFont.Bold))
        title_label.setStyleSheet("color: #00ff00;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Create a container for proper centering
        title_container = QWidget()
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        title_container_layout.addWidget(title_label)
        
        # Add the title container with stretch factors for perfect centering
        title_bar_layout.addWidget(title_container, 1)  # Takes all available space
        
        # Set this as the menu bar (acts as title bar)
        self.setMenuWidget(title_bar)
        
        # Setup the main UI
        self.setup_ui()
        
    def setup_ui(self):
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 20, 30, 20)
        self.layout.setSpacing(15)
        
        # Game header
        self.setup_header()
        
        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #00ff00;")
        self.layout.addWidget(divider)
        
        # Challenge title
        challenge_title = QLabel("PASSWORD SECURITY CHALLENGE")
        challenge_title.setAlignment(Qt.AlignCenter)
        challenge_title.setFont(QFont("Consolas", 22, QFont.Bold))
        challenge_title.setStyleSheet("margin: 40px;")  # Adds 20px top margin
        self.layout.addWidget(challenge_title)
        
        # Password creation section
        pwd_label = QLabel("CREATE SECURE PASSWORD:")
        pwd_label.setFont(QFont("Consolas", 10))
        self.layout.addWidget(pwd_label)
        
        self.pwd_input = QLineEdit()
        self.pwd_input.setFont(QFont("Consolas", 10))
        self.pwd_input.setStyleSheet("""
            QLineEdit {
                background-color: #282828;
                color: #00ff00;
                border: 2px solid #00aa00;
                border-radius: 10px;
                padding: 8px;
                min-height: 25px;
            }
        """)
        self.pwd_input.textChanged.connect(self.check_password)
        self.layout.addWidget(self.pwd_input)
        
        # Password strength indicator
        strength_layout = QHBoxLayout()
        strength_layout.setSpacing(10)
        
        self.pwd_strength = QProgressBar()
        self.pwd_strength.setFont(QFont("Consolas", 8))
        self.pwd_strength.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00aa00;
                border-radius: 15px;
                background: #282828;
                height: 24px;
                padding: 0px;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                border-radius: 15px;
            }
        """)
        self.pwd_strength.setTextVisible(False)  # Hide percentage text
        strength_layout.addWidget(self.pwd_strength, 1)
        
        self.strength_label = QLabel("WEAK")
        self.strength_label.setFont(QFont("Consolas", 10))
        self.strength_label.setStyleSheet("color: #ff5555;")
        strength_layout.addWidget(self.strength_label)
        
        self.layout.addLayout(strength_layout)
        
        # Feedback box (the "cube" under input)
        self.result_text = QLabel("CHALLENGE COMPLETE! Moving to next challenge...")
        self.result_text.setFont(QFont("Consolas", 10))
        self.result_text.setStyleSheet("""
            QLabel {
                background-color: #282828;
                color: #00ff00;
                border: 2px solid #00aa00;
                border-radius: 10px;
                padding: 12px;
                min-height: 120px;
            }
        """)
        self.result_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.result_text.setWordWrap(True)
        self.layout.addWidget(self.result_text)
        
       # Submit button
        submit_button = QPushButton("SUBMIT")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #003300;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 10px;
                font-weight: bold;
                min-width: 200px;
                margin-top : 40px ;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
            }
        """)
        submit_button.clicked.connect(self.submit_password)
        self.layout.addWidget(submit_button, 0, Qt.AlignCenter)
        
        self.layout.addStretch()
    
    
    def setup_header(self):
        """Setup the game header with title, agent info, score, etc."""

        
        # Agent info
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("AGENT: DEFENDER_42"))
        info_layout.addWidget(QLabel(f"SCORE: {self.score}"))
        info_layout.addWidget(QLabel("LEVEL: 01"))
        
        # Set equal spacing
        for i in range(info_layout.count()):
            item = info_layout.itemAt(i)
            if item.widget():
                item.widget().setStyleSheet("color: #00ff00;")
        
        self.layout.addLayout(info_layout)
    
    def check_password(self):
        """Check password strength and update UI"""
        password = self.pwd_input.text()
        strength, feedback = self.check_password_strength(password)
        
        # Update progress bar and label
        self.pwd_strength.setValue(strength)
        
        if strength < 50:
            self.strength_label.setText("WEAK")
            self.strength_label.setStyleSheet("color: #ff0000;")
            self.pwd_strength.setStyleSheet("""
                QProgressBar {border: 1px solid #00ff00; background-color: #333333;}
                QProgressBar::chunk {background-color: #ff0000;}
            """)
        elif strength < 80:
            self.strength_label.setText("MEDIUM")
            self.strength_label.setStyleSheet("color: #ffaa00;")
            self.pwd_strength.setStyleSheet("""
                QProgressBar {border: 1px solid #00ff00; background-color: #333333;}
                QProgressBar::chunk {background-color: #ffaa00;}
            """)
        else:
            self.strength_label.setText("STRONG")
            self.strength_label.setStyleSheet("color: #00ff00;")
            self.pwd_strength.setStyleSheet("""
                QProgressBar {border: 1px solid #00ff00; background-color: #333333;}
                QProgressBar::chunk {background-color: #00ff00;}
            """)
        
        self.result_text.setText("\n".join(feedback))
    
    def submit_password(self):
        password = self.pwd_input.text()
        strength, feedback = self.check_password_strength(password)
        
        if not password:
            self.result_text.setText("ERROR: Password cannot be empty!")
            return
            
        points = strength
        self.score += points
        self.update_score()
        
        if strength < 50:
            feedback.insert(0, f"Password too weak! +{points} points")
        elif strength < 80:
            feedback.insert(0, f"Good password! +{points} points")
        else:
            feedback.insert(0, f"Excellent password! +{points} points")
            self.challenge_complete.emit(points)  # 🔥 EMIT SIGNAL HERE

    def complete_challenge(self):
        """Handle successful challenge completion by opening next window"""
        self.result_text.setText("CHALLENGE COMPLETE! Opening next challenge...")
    
        self.next_window = NextChallenge()  # or PhishingEmailChallenge() when it's ready
        self.next_window.show()
        self.close()  # Close the current window
    
    
    def update_score(self):
        """Update score display"""
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if isinstance(item, QHBoxLayout):  # This is our info layout
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if widget and "SCORE:" in widget.text():
                        widget.setText(f"SCORE: {self.score}")
                        break
    
    
    def check_password_strength(self, password):
        """
        Simplified password strength checker
        Returns score (0-100) and feedback list
        """
        feedback = []
        score = 0
        
        # Length check (8+ characters)
        if len(password) < 8:
            feedback.append("- Must be at least 8 characters")
            return 0, feedback
        else:
            score += 25
            feedback.append("+ Good length")
        
        # Character variety checks
        checks = [
            (r'[A-Z]', "uppercase letter", 15),
            (r'[a-z]', "lowercase letter", 15),
            (r'[0-9]', "number", 15),
            (r'[^A-Za-z0-9]', "special character", 15)
        ]
        
        for pattern, description, points in checks:
            if re.search(pattern, password):
                score += points
                feedback.append(f"+ Contains {description}")
            else:
                feedback.append(f"- Missing {description}")
        
        # Bonus for length
        if len(password) >= 12:
            score += 15
            feedback.append("+ Bonus for long password")
        
        # Ensure score is 0-100
        score = max(0, min(100, score))
        
        return score, feedback