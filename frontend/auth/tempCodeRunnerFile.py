import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QHBoxLayout, QFrame
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
        # Resize the rectangle when screen size changes
     if hasattr(self, 'box_frame'):
        self.box_frame.setFixedWidth(int(self.width() * 0.7))

    def init_ui(self):
        green = "#00FF00"
        darker_green = "#003300"

        # Main Rectangle Box
        self.box_frame = QFrame()
        self.box_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {green};
                background-color: black;
            }}
        """)
        box_layout = QVBoxLayout(self.box_frame)

        # Registration Title Inside Box
        reg_label = QLabel("AGENT REGISTRATION")
        reg_label.setFont(QFont("Courier", 14, QFont.Bold))
        reg_label.setStyleSheet(f"""
            color: {green};
            background-color: {darker_green};
            padding: 8px;
        """)
        reg_label.setAlignment(Qt.AlignCenter)

        # Username
        user_label = QLabel("USERNAME:")
        user_label.setFont(QFont("Courier", 10))
        user_label.setStyleSheet(f"color: {green};")

        # Password
        pass_label = QLabel("PASSWORD:")
        pass_label.setFont(QFont("Courier", 10))
        pass_label.setStyleSheet(f"color: {green};")
        pass_input = QLineEdit()
        pass_input.setEchoMode(QLineEdit.Password)
        pass_input.setStyleSheet(f"color: {green}; background-color: black; border: 1px solid {green};")

        # Security Level
        sec_label = QLabel("SECURITY LEVEL:")
        sec_label.setFont(QFont("Courier", 10))
        sec_label.setStyleSheet(f"color: {green};")
        sec_combo = QComboBox()
        sec_combo.addItems(["BEGINNER", "INTERMEDIATE", "ADVANCED"])
        sec_combo.setStyleSheet(f"color: {green}; background-color: black; border: 1px solid {green};")

        # Department
        dep_label = QLabel("DEPARTMENT:")
        dep_label.setFont(QFont("Courier", 10))
        dep_label.setStyleSheet(f"color: {green};")
        dep_combo = QComboBox()
        dep_combo.addItems(["IT OPERATIONS", "HR", "FINANCE", "ENGINEERING"])
        dep_combo.setStyleSheet(f"color: {green}; background-color: black; border: 1px solid {green};")

        # Button
        init_btn = QPushButton("INITIALIZE TRAINING")
        init_btn.setFont(QFont("Courier", 10))
        init_btn.setStyleSheet(f"""
            QPushButton {{
                color: {green};
                background-color: black;
                border: 1px solid {green};
                padding: 6px;
            }}
            QPushButton:hover {{
                background-color: {green};
                color: black;
            }}
        """)

        # Add elements to box layout
        box_layout.addWidget(reg_label)
        box_layout.addSpacing(10)
        box_layout.addWidget(user_label)
        box_layout.addWidget(user_input)
        box_layout.addWidget(pass_label)
        box_layout.addWidget(pass_input)
        box_layout.addWidget(sec_label)
        box_layout.addWidget(sec_combo)
        box_layout.addWidget(dep_label)
        box_layout.addWidget(dep_combo)
        box_layout.addSpacing(10)
        box_layout.addWidget(init_btn)

        # Title
        title = QLabel("CYBERDEFEND")
        title.setFont(QFont("Courier", 32, QFont.Bold))
        title.setStyleSheet(f"color: {green};")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("SECURITY AWARENESS TRAINING")
        subtitle.setFont(QFont("Courier", 14))
        subtitle.setStyleSheet(f"color: {green};")
        subtitle.setAlignment(Qt.AlignCenter)

        # Center Layout
        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(30)

        box_container = QHBoxLayout()
        box_container.addStretch()
        box_container.addWidget(self.box_frame)
        box_container.addStretch()

        main_layout.addLayout(box_container)
        main_layout.addStretch()

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CyberDefendApp()
    win.show()
    sys.exit(app.exec_())
