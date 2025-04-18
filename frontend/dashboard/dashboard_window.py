import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CyberDefendDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberDefend - Security Awareness Training")
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")
        self.init_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def init_ui(self):
        green = "#00FF00"
        darker_green = "#003300"
        gray = "#666666"
        red = "#FF0000"
        dark_gray = "#1a1a1a"  # Dark gray for mission box background
        

        def styled_label(text, font_size=12, bold=False, align=Qt.AlignLeft, color=green):
            label = QLabel(text)
            font = QFont("Courier", font_size)
            font.setBold(bold)
            label.setFont(font)
            label.setStyleSheet(f"color: {color}; padding: 5px;")
            label.setAlignment(align)
            return label

        # Title label (will be placed between left and right containers)
        title = styled_label("CYBERDEFEND", 70 , True, Qt.AlignCenter)
        subtitle = styled_label("SECURITY AWARENESS TRAINING", 20, False, Qt.AlignCenter)

        # Left Info Box
        left_info_frame = QFrame()
        left_info_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {green};
                padding: 10px;
                border-radius: 10px;
                background-color: black; 
            }}
        """)
        left_info_layout = QVBoxLayout(left_info_frame)
        left_info_layout.setSpacing(10)
        left_info_text = QLabel("AGENT: DEFENDER_42\nDEPARTEMENT: IT")
        left_info_text.setFont(QFont("Courier", 12))
        left_info_text.setStyleSheet(f"color: {green}; border: none;")
        left_info_layout.addWidget(left_info_text)

        left_container = QWidget()
        left_container_layout = QVBoxLayout(left_container)
        left_container_layout.setContentsMargins(0, 0, 0, 0)
        left_container_layout.addWidget(left_info_frame)

        # Right Info Box with random text
        right_info_frame = QFrame()
        right_info_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {green};
                padding: 10px;
                border-radius: 10px;
                background-color: black; 
            }}
        """)
        right_info_layout = QVBoxLayout(right_info_frame)
        right_info_layout.setSpacing(10)
        right_info_text = QLabel("RANK: NOVICE\nXP: 1250/5000")
        right_info_text.setFont(QFont("Courier", 12))
        right_info_text.setStyleSheet(f"color: {green}; border: none;")
        right_info_layout.addWidget(right_info_text)

        right_container = QWidget()
        right_container_layout = QVBoxLayout(right_container)
        right_container_layout.setContentsMargins(0, 0, 0, 0)
        right_container_layout.addWidget(right_info_frame)

        # Central container for title and subtitle
        central_container = QWidget()
        central_layout = QVBoxLayout(central_container)
        central_layout.addWidget(title)
        central_layout.addWidget(subtitle)
        central_layout.setAlignment(Qt.AlignCenter)

        # Create a horizontal container for left container, title, and right container
        top_horizontal_container = QWidget()
        top_horizontal_layout = QHBoxLayout(top_horizontal_container)
        top_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        top_horizontal_layout.setSpacing(50)  # space between containers and title

        # Add left container, title, and right container to the horizontal layout
        top_horizontal_layout.addWidget(left_container, alignment=Qt.AlignLeft)
        top_horizontal_layout.addWidget(central_container, alignment=Qt.AlignCenter)
        top_horizontal_layout.addWidget(right_container, alignment=Qt.AlignRight)

        # Subtitle below the horizontal container
        subtitle.setFixedHeight(30)

        # Main container to center content
        main_container = QWidget()
        main_container.setStyleSheet("background-color: transparent;")
        main_container_layout = QVBoxLayout(main_container)
        main_container_layout.setContentsMargins(0, 0, 0, 0)

        # Add the horizontal container and subtitle to main container
        main_container_layout.addWidget(top_horizontal_container)
        main_container_layout.addSpacing(20)

        # Missions Section Title
        mission_title = QLabel("MISSION SELECTION")
        mission_title.setFont(QFont("Courier", 16, QFont.Bold))
        mission_title.setStyleSheet(f"""
            color: {green};
            background-color: {dark_gray};
            padding: 12px;
            border-radius: 0px;
        """)
        mission_title.setAlignment(Qt.AlignCenter)

        # Missions Grid
        mission_grid = QGridLayout()
        mission_grid.setContentsMargins(10, 10, 10, 10)  # Reduced margins
        mission_grid.setSpacing(10)  # Reduced spacing

        def create_mission_box(title, desc, locked=False, special=False):
            color = gray if locked else (red if special else green)
            border_style = "dashed" if special else "solid"

            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    border: 1px {border_style} {color};
                    padding: 10px;
                    border-radius: 8px;
                    background-color: {dark_gray};
                }}
            """)
            layout = QVBoxLayout(frame)
            layout.setSpacing(8)

            # Title Label (bold and bigger)
            title_label = QLabel(title)
            title_font = QFont("Courier", 14)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet(f"color: {color}; border:none;")
            title_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(title_label)

            # Description Label 
            desc_label = QLabel(desc)
            desc_font = QFont("Courier", 11)
            desc_label.setFont(desc_font)
            desc_label.setStyleSheet(f"color: {color}; border:none;")
            desc_label.setAlignment(Qt.AlignLeft)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

            # Start/Locked Button
            button = QPushButton("LOCKED" if locked else ("CLASSIFIED" if special else "START"))
            button.setEnabled(not locked)
            button.setFont(QFont("Courier", 11))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {color};
                    border: 1px solid {color};
                    padding: 6px;
                }}
                QPushButton:disabled {{
                    color: {gray};
                    border: 1px solid {gray};
                }}
            """)
            layout.addWidget(button, alignment=Qt.AlignRight)

            return frame

        # Add mission boxes
        mission_grid.addWidget(create_mission_box("LEVEL 1: PHISHING DEFENSE",
                                                  "Learn to identify and respond to common phishing attempts."), 0, 0)
        mission_grid.addWidget(create_mission_box("LEVEL 2: PASSWORD SECURITY",
                                                  "Create strong passwords and avoid common password vulnerabilities."), 0, 1)
        mission_grid.addWidget(create_mission_box("LEVEL 3: SOCIAL ENGINEERING",
                                                  "Detect and counter social engineering attacks."), 1, 0)
        mission_grid.addWidget(create_mission_box("LEVEL 4: MALWARE RESPONSE",
                                                  "Identify and respond to various malware threats.", locked=True), 1, 1)

        # Central Box - thinned border
        box_frame = QFrame()
        box_frame.setStyleSheet(f"""
            QFrame {{
                border: 1px solid {green};  
                border-radius: 10px;
                background-color: black;
            }}
        """)
        box_layout = QVBoxLayout(box_frame)
        box_layout.setContentsMargins(5, 5, 5, 5)  # Remove internal padding
        box_layout.addWidget(mission_title)
        box_layout.addLayout(mission_grid)
        
        # Add mission box to main container
        main_container_layout.addWidget(box_frame)

        # Final Layout
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(main_container, alignment=Qt.AlignCenter)
        main_layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberDefendDashboard()
    window.show()
    sys.exit(app.exec_())
