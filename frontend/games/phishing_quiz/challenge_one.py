from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QCheckBox, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QSizePolicy


class PhishingEmailChallenge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add header
        self.add_header(main_layout)

        # Content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Left column - Checklist (30%) with border
        left_column = QWidget()
        left_column.setStyleSheet("""
            background-color: #1a1a1a;
            border: 2px solid #00aa00;
            border-radius: 5px;
        """)
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        issues_title = QLabel("IDENTIFY ISSUES:")
        issues_title.setFont(QFont("Consolas", 12, QFont.Bold))
        issues_title.setStyleSheet("""
            QLabel {
                color: #00ff00;
                background-color: transparent;
                border: none;
                font: bold 12pt Consolas;
                margin-bottom: 10px;
            }
        """)
        

        left_layout.addWidget(issues_title)

        # Checkboxes
        self.checks = []
        self.checkbox_group = QButtonGroup(self)  # Create a QButtonGroup
        for text in ["Sender Email", "URL Issues", "Urgency", "Threats", "Grammar", "Logo Issues"]:
            box = QCheckBox(text)
            box.setFont(QFont("Consolas", 10))
            # Inside the for loop creating the checkboxes:
            box.setStyleSheet("""
                QCheckBox {
                    color: #00ff00;
                    background-color: transparent;
                    spacing: 10px;
                    margin: 8px 0;
                    border: none;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    background: #000000;
                    border: 2px solid #00ff00;
                }
                QCheckBox::indicator:checked {
                    background-color: #00ff00;
                }
            """)

            self.checkbox_group.addButton(box)  # Add each checkbox to the group
            self.checks.append(box)
            left_layout.addWidget(box)
        
        left_layout.addStretch()
        content_layout.addWidget(left_column, 30)

        # Right column - Email (70%) with a single border
        right_column = QWidget()
        right_column.setStyleSheet("""
            background-color: #000000;
            border: 2px solid #00ff00;
            border-radius: 5px;
            /* Remove padding here */
        """)
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(15, 15, 15, 15)


        # Email display
        email_box = QLabel()
        email_box.setFont(QFont("Consolas", 11))
        email_box.setStyleSheet("color: #00ff00; background-color: transparent; border: none;")
        email_box.setText(
            "From: security-check@paypal-alert.com\n"
            "To: defender42@company.com\n"
            "Subject: [ACTION REQUIRED] Confirm Your PayPal Login\n"
            "Date: April 14, 2025, 10:45:02\n\n\n"
            "Dear User,\n\n"
            "We have detected a login attempt from a new device in Russia. If this was not you,\n"
            "please secure your account immediately to avoid unauthorized access.\n\n"
            "To verify and secure your account, click the link below:\n"
            "https://secure-paypal-check.com/login\n\n"
            "If no action is taken in the next 12 hours, your account will be permanently locked.\n\n"
            "Thanks for choosing PayPal Security Team."
        )
        email_box.setWordWrap(True)
        right_layout.addWidget(email_box)
        content_layout.addWidget(right_column, 70)

        main_layout.addWidget(content_widget)

        # Response section - completely borderless
        response_widget = QWidget()
        response_widget.setStyleSheet("background-color: transparent;")
        response_layout = QVBoxLayout(response_widget)
        response_layout.setContentsMargins(20, 15, 20, 15)

        response_title = QLabel("SELECT APPROPRIATE RESPONSE:")
        response_title.setFont(QFont("Consolas", 12, QFont.Bold))
        response_title.setStyleSheet("color: #00ff00; margin-bottom: 10px;")
        response_layout.addWidget(response_title)

        btn_container = QWidget()
        btn_container.setStyleSheet("background-color: transparent;")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        # Before the loop
        self.response_button_group = QButtonGroup(self)
        self.response_button_group.setExclusive(True)
        
        # In the for loop creating response buttons:
        for text, option in [("A) CLICK LINK", "click"), 
                             ("B) DELETE", "delete"), 
                             ("C) REPLY", "reply")]:
            btn = QPushButton(text)
            btn.setFont(QFont("Consolas", 10, QFont.Bold))
            btn.setCheckable(True)  # Make the button checkable
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #003300;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    padding: 12px 0;
                    margin: 0 10px;
                    min-width: 200px;
                }
                QPushButton:hover, QPushButton:checked {
                    background-color: #00ff00;
                    color: #000000;
                }
            """)
            btn.clicked.connect(lambda _, o=option: self.handle_response(o))
            self.response_button_group.addButton(btn)  # Add to the group
            btn_layout.addWidget(btn)

        
        response_layout.addWidget(btn_container)
        main_layout.addWidget(response_widget)

                
        submit_btn = QPushButton("SUBMIT")
        submit_btn.setFont(QFont("Consolas", 10, QFont.Bold))
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #003300;
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 12px 100px;  /* increase horizontal padding */
                margin: 20px 10px 0 10px;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
            }
        """)
        submit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        response_layout.addWidget(submit_btn, alignment=Qt.AlignCenter)


    def add_header(self, layout):
        """Create and add the header widget"""
        header = QWidget()
        header.setStyleSheet("background-color: #282828;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)

        # Colored dots
        dots = QWidget()
        dots_layout = QHBoxLayout(dots)
        dots_layout.setSpacing(8)
        for color in ["#FF5F56", "#FFBD2E", "#27C93F"]:
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            dots_layout.addWidget(dot)
        
        # Title
        title = QLabel("CYBERDEFEND PROTOCOL v2.7.1")
        title.setFont(QFont("Consolas", 10, QFont.Bold))
        title.setStyleSheet("color: #00ff00;")

        # Game info
        info = QWidget()
        info_layout = QHBoxLayout(info)
        info_layout.addWidget(QLabel("AGENT: DEFENDER_42"))
        info_layout.addWidget(QLabel("SCORE: 2450"))
        info_layout.addWidget(QLabel("LEVEL: 01"))
        info_layout.addWidget(QLabel("LIVES: 3"))
        for i in range(info_layout.count()):
            w = info_layout.itemAt(i).widget()
            w.setStyleSheet("color: #00ff00; font-family: Consolas;")

        header_layout.addWidget(dots)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(info)

        layout.addWidget(header)

    def handle_response(self, option):
        """Handle response button clicks"""
        if option == "click":
            print("User chose to click link")
        elif option == "delete":
            print("User chose to delete email")
        elif option == "reply":
            print("User chose to reply")

    def handle_submit(self):
        selected_button = self.response_button_group.checkedButton()
        if selected_button:
            print("User selected: ", selected_button.text())
        else:
            print("No option selected!")
