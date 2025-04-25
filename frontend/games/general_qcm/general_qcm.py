from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QButtonGroup, QRadioButton, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import winsound
import ctypes
from games.social_engineering.social_engineering_data import CHALLENGES


class GameWindow(QWidget):
    def __init__(self, challenges, gamer_info):
        super().__init__()
        self.challenges = challenges
        self.gamer_info = gamer_info
        self.current_index = 0
        self.score = 0
        self.difficulty = 1
        self.time_left = 60 
        self.sound_on = True
        self.tool_used = False
        self.init_ui()
        self.prevent_screenshot()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1200, 800)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top Bar Layout
        top_bar = QHBoxLayout()

        self.info_label = QLabel(
            f"👤 Player: {self.gamer_info['name']} | 🏢 Dept: {self.gamer_info['department']} | 🏆 Score: {self.score}"
        )
        self.info_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #DDD;")
        top_bar.addWidget(self.info_label)

        top_bar.addStretch()

        toggle_layout = QHBoxLayout()

        self.sound_toggle = QPushButton("🔊 ON")
        self.sound_toggle.clicked.connect(self.toggle_sound)
        toggle_layout.addWidget(self.sound_toggle)

        top_bar.addLayout(toggle_layout)
        top_bar.addStretch()

        timer_container = QHBoxLayout()
        self.timer_label = QLabel(f"⏱️ {self.time_left} sec")
        self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00FF00;")
        timer_container.addWidget(self.timer_label)

        self.pause_button = QPushButton("⏸")
        self.pause_button.setFixedSize(30, 30)
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setStyleSheet("font-weight: bold;")
        timer_container.addWidget(self.pause_button)

        self.paused_label = QLabel("")
        self.paused_label.setStyleSheet("font-size: 14px; color: red; margin-left: 10px;")
        timer_container.addWidget(self.paused_label)

        top_bar.addLayout(timer_container)
        self.layout.addLayout(top_bar)

        # Scenario Box
        # Scenario Box
        self.scenario_frame = QFrame()
        self.scenario_frame.setFrameShape(QFrame.Box)
        self.scenario_frame.setStyleSheet("""
    QFrame {
        border: 2px solid #00FF00;
        background-color: black;
        margin-top: 20px;
        margin-bottom: 10px;
    }
""")

        self.scenario_label = QLabel()
        self.scenario_label.setWordWrap(True)
        self.scenario_label.setStyleSheet("QLabel { border: none; padding: 10px; }")  # no extra box here
        frame_layout = QVBoxLayout(self.scenario_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)  # no extra padding inside the box
        frame_layout.addWidget(self.scenario_label)

        self.layout.addWidget(self.scenario_frame)
        self.response_title = QLabel(" What to do?")
        self.response_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.layout.addWidget(self.response_title)

        self.response_group = QButtonGroup(self)
        self.response_buttons = QVBoxLayout()
        self.layout.addLayout(self.response_buttons)

        self.submit_button = QPushButton("Submit Response")
        self.submit_button.clicked.connect(self.check_response)
        self.layout.addWidget(self.submit_button)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.exit_button = QPushButton(" Exit")
        self.exit_button.setObjectName("exitButton")
        self.exit_button.clicked.connect(self.close_game)
        bottom_layout.addWidget(self.exit_button)
        self.layout.addLayout(bottom_layout)

        self.set_dark_mode()
        self.load_challenge()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def set_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: #00FF00;
                font-family: Consolas;
                font-size: 20px;
            }
            QLabel {
                color: #00FF00;
            }
            QRadioButton {
                color: #00FF00;
                border: 2px solid #00FF00;
                padding: 6px;
                width: 200px;
            }
            QRadioButton::indicator {
                width: 0px;
                height: 0px;
            }
            QRadioButton:checked {
                background-color: #00FF00;
                color: black;
            }
            QRadioButton:unchecked {
                background-color: transparent;
                color: #00FF00;
            }
            QPushButton {
                background-color: #003300;
                color: #00FF00;
                border: 1px solid #00FF00;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #005500;
            }
            QPushButton#exitButton {
                background-color: #550000;
                color: #FFFFFF;
                padding: 4px 10px;
                min-width: 100px;
                font-size: 12px;
            }
            QPushButton#exitButton:hover {
                background-color: #FF0000;
            }
        """)
        self.dark_mode = True

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("▶")
            self.paused_label.setText("⏸ Paused")
            self.submit_button.setDisabled(True)
            for btn in self.response_group.buttons():
                btn.setDisabled(True)
        else:
            self.timer.start(1000)
            self.pause_button.setText("⏸")
            self.paused_label.setText("")
            self.submit_button.setDisabled(False)
            for btn in self.response_group.buttons():
                btn.setDisabled(False)

    def load_challenge(self):
        self.tool_used = False
        if self.current_index >= len(self.challenges):
            self.show_summary()
            return

        challenge = self.challenges[self.current_index]
        self.scenario_label.setText(f"Scenario:\n\n{challenge['scenario']}")

        for i in reversed(range(self.response_buttons.count())):
            widget = self.response_buttons.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.response_group = QButtonGroup(self)
        for response in challenge['responses']:
            btn = QRadioButton(response)
            btn.setToolTip(challenge.get('responses_info', {}).get(response, ''))
            self.response_group.addButton(btn)
            self.response_buttons.addWidget(btn)

        self.update_info()

    def check_response(self):
        selected_response_btn = self.response_group.checkedButton()
        if not selected_response_btn:
            return

        selected_response = selected_response_btn.text()
        challenge = self.challenges[self.current_index]
        correct_response = challenge['correct_response']

        if selected_response != correct_response:
            selected_response_btn.setStyleSheet("background-color: #FF0000; color: white; border: 2px solid #FF0000;")

        self.play_sound("incorrect")
        QMessageBox.critical(self, "Incorrect", f"\nCorrect Response: {correct_response}", buttons=QMessageBox.Ok)
        self.current_index += 1
        self.time_left = 60
        self.load_challenge()

    def show_summary(self):
        QMessageBox.information(self, "Game Over", f"Well done, {self.gamer_info['name']}! Your total score is {self.score}.")
        self.close()

    def update_info(self):
        self.info_label.setText(f"Player: {self.gamer_info['name']} | Dept: {self.gamer_info['department']} | Score: {self.score}")

    def play_sound(self, result):
        if not self.sound_on:
            return
        if result == "correct":
            winsound.Beep(1000, 500)
        else:
            winsound.Beep(500, 500)

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        status = "ON" if self.sound_on else "OFF"
        self.sound_toggle.setText(f"Sound: {status}")

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time Left: {self.time_left} sec")
        if self.time_left == 0:
            QMessageBox.warning(self, "Time's Up", "You ran out of time for this challenge!")
            self.current_index += 1
            self.time_left = 60
            self.load_challenge()

    def close_game(self):
        response = QMessageBox.question(self, "Exit Game", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            self.close()

    def prevent_screenshot(self):
        hwnd = int(self.winId())
        try:
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 1)
        except Exception as e:
            print(f"Screenshot protection not supported: {e}")
