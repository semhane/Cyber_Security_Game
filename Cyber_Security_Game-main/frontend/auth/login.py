import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QFrame, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CyberDefendLoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberDefend - Login")
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")
        self.init_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def resizeEvent(self, event):
        if hasattr(self, 'box_frame'):
            self.box_frame.setFixedWidth(int(self.width() * 0.5))

    def init_ui(self):
        # Define colors
        green = "#00FF00"
        darker_green = "#003300"

        # Custom Title Bar
        title_label = QLabel("CYBERDEFEND")
        title_font = QFont("Arial", 65, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {green};")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("SECURITY AWARENESS TRAINING")
        subtitle_font = QFont("Courier", 36, QFont.Normal)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {green};")
        subtitle.setAlignment(Qt.AlignCenter)

        # Main Rectangle Box
        self.box_frame = QFrame()
        self.box_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {green};
                background-color: black;
                border-radius: 10px;
            }}
        """)
        self.box_frame.setFixedWidth(int(self.width() * 0.5))
        box_layout = QVBoxLayout(self.box_frame)

        # Title inside box
        login_label = QLabel("AGENT LOGIN")
        login_label.setFont(QFont("Courier", 16, QFont.Bold))
        login_label.setStyleSheet(f"""
            color: {green};
            background-color: {darker_green};
            padding: 12px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        """)
        login_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(login_label)

        label_style = f"""
            color: {green};
            background-color: transparent;
            font: bold 12pt Courier;
            padding: 0px;
            border: none;
        """

        # Input Style
        input_style = f"""
            color: {green};
            background-color: black;
            border: 1px solid {green};
            padding: 10px;
            font-size: 14px;
        """

        def add_field(layout, label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet(label_style)
            label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            layout.addWidget(label)
            layout.addWidget(widget)

        # Form Area
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(20, 20, 20, 20)  # Add some padding inside the box

        # Input fields
        username_or_email_input = QLineEdit()
        username_or_email_input.setStyleSheet(input_style)

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet(input_style)

        add_field(form_layout, "EMAIL/USERNAME:", username_or_email_input)
        add_field(form_layout, "PASSWORD:", password_input)

        # Links container (horizontal layout for Sign Up and Forgot Password)
        links_layout = QHBoxLayout()
        
        # Sign Up link on the left
        signup_label = QLabel("<a href='#' style='text-decoration: none; color: #00FF00; background-color: transparent;'>Sign Up</a>")
        signup_label.setStyleSheet(f"color: {green}; font: bold 12pt Courier;border:none")
        signup_label.setOpenExternalLinks(True)
        links_layout.addWidget(signup_label)
        
        # Spacer to push Forgot Password to the right
        links_layout.addStretch()
        
        # Forgot Password link on the right
        forgot_password_label = QLabel("<a href='#' style='text-decoration: none; color: #00FF00; background-color: transparent;'>Forgot Password?</a>")
        forgot_password_label.setStyleSheet(f"color: {green}; font: bold 12pt Courier;border:none")
        forgot_password_label.setOpenExternalLinks(True)
        links_layout.addWidget(forgot_password_label)
        
        form_layout.addLayout(links_layout)

        box_layout.addLayout(form_layout)

        # Button
        login_btn = QPushButton("LOGIN")
        login_btn.setFont(QFont("Courier", 12))
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {green};
                color: black;
                border: 1px solid {green};
                padding: 10px;
                margin: 20px;
            }}
            QPushButton:hover {{
                color: {green};
                background-color: black;
            }}
        """)
        box_layout.addWidget(login_btn)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title_label)
        center_layout.addWidget(subtitle)
        center_layout.addSpacing(20)
        center_layout.addWidget(self.box_frame)

        # Outer layout
        outer_layout = QVBoxLayout(self)
        outer_layout.addStretch()
        outer_layout.addLayout(center_layout)
        outer_layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CyberDefendLoginApp()
    win.show()
    sys.exit(app.exec_())