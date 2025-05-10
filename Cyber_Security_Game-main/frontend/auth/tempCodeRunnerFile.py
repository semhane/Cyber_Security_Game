import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CyberDefendApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberDefend - Security Awareness Training")
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
        reg_label = QLabel("AGENT REGISTRATION")
        reg_label.setFont(QFont("Courier", 16, QFont.Bold))
        reg_label.setStyleSheet(f"""
            color: {green};
            background-color: {darker_green};
            padding: 12px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        """)
        reg_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(reg_label)

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

        username_input = QLineEdit()
        username_input.setStyleSheet(input_style)

        email_input = QLineEdit()
        email_input.setStyleSheet(input_style)

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet(input_style)

        security_combo = QComboBox()
        security_combo.addItems(["BEGINNER", "INTERMEDIATE", "ADVANCED"])
        security_combo.setStyleSheet(input_style)

        department_combo = QComboBox()
        department_combo.addItems(["IT OPERATIONS", "HR", "FINANCE", "ENGINEERING"])
        department_combo.setStyleSheet(input_style)

        add_field(form_layout, "USERNAME:", username_input)
        add_field(form_layout, "EMAIL:", email_input)
        add_field(form_layout, "PASSWORD:", password_input)
        add_field(form_layout, "SECURITY LEVEL:", security_combo)
        add_field(form_layout, "DEPARTMENT:", department_combo)

        box_layout.addLayout(form_layout)

        # Button
        box_layout.addSpacing(15)
        init_btn = QPushButton("INITIALIZE TRAINING")
        init_btn.setFont(QFont("Courier", 12))
        init_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {green};
                color: black;
                border: 1px solid {green};
                padding: 10px;
            }}
            QPushButton:hover {{
                color: {green};
                background-color: black;
            }}
        """)
        box_layout.addWidget(init_btn)

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
    win = CyberDefendApp()
    win.show()
    sys.exit(app.exec_())
