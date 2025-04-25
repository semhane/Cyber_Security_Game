from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
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
        self.difficulty = 1  # Easy difficulty by default
        self.time_left = 60 
        self.sound_on = True
        self.tool_used = False
          # Default theme is dark mode
        self.init_ui()
        self.prevent_screenshot()

    def init_ui(self):
     self.setWindowFlags(Qt.FramelessWindowHint)
     self.resize(1200, 800)

     self.layout = QVBoxLayout()
     self.setLayout(self.layout)

    # --- Top Bar Layout ---
     top_bar = QHBoxLayout()

    # Player info label
     self.info_label = QLabel(
        f"👤 Player: {self.gamer_info['name']} | 🏢 Dept: {self.gamer_info['department']} | 🏆 Score: {self.score}"
    )
     self.info_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #DDD;")
     top_bar.addWidget(self.info_label)

     top_bar.addStretch()

# Toggle Buttons (center)
     toggle_layout = QHBoxLayout()

# Sound toggle button
     self.sound_toggle = QPushButton("🔊 ON")
     self.sound_toggle.clicked.connect(self.toggle_sound)
     toggle_layout.addWidget(self.sound_toggle)


# Add to top bar layout
     top_bar.addLayout(toggle_layout)
     top_bar.addStretch()


    # Right: Timer + Pause
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

    # --- Scenario Box ---
     self.scenario_box = QWidget()
     self.scenario_box.setObjectName("scenario_box")
     self.scenario_layout = QVBoxLayout()
     self.scenario_label = QLabel()
     self.scenario_label.setWordWrap(True)
     self.scenario_layout.addWidget(self.scenario_label)
     self.scenario_box.setLayout(self.scenario_layout)
     self.layout.addWidget(self.scenario_box)

    # --- Red Flags Box ---
     self.redflags_box = QWidget()
     self.redflags_box.setObjectName("redflags_box")
     self.redflags_layout = QVBoxLayout()
     self.red_flags_label = QLabel("🚩 Red Flags")
     self.red_flags_label.setWordWrap(True)
     self.redflags_layout.addWidget(self.red_flags_label)
     self.flag_list = QLabel()
     self.flag_list.setWordWrap(True)
     self.redflags_layout.addWidget(self.flag_list)
     self.redflags_box.setLayout(self.redflags_layout)
     self.layout.addWidget(self.redflags_box)

    # --- Response Buttons ---
     self.response_title = QLabel("🧠 What to do?")
     self.response_title.setStyleSheet("font-weight: bold; font-size: 18px; margin-top: 15px;")
     self.layout.addWidget(self.response_title)

     self.response_group = QButtonGroup(self)
     self.response_buttons = QVBoxLayout()
     self.layout.addLayout(self.response_buttons)


    # --- Submit Button ---
     self.submit_button = QPushButton("Submit Response")
     self.submit_button.clicked.connect(self.check_response)
     self.layout.addWidget(self.submit_button)

    # --- Tools ---
     self.tools_label = QLabel("🛠️ Tools:")
     self.layout.addWidget(self.tools_label)
     self.tools_layout = QHBoxLayout()
     self.layout.addLayout(self.tools_layout)

    # --- Bottom Layout ---
     bottom_layout = QHBoxLayout()
     bottom_layout.addStretch()
     self.exit_button = QPushButton("❌ Exit")
     self.exit_button.setObjectName("exitButton")
     self.exit_button.clicked.connect(self.close_game)
     bottom_layout.addWidget(self.exit_button)
     self.layout.addLayout(bottom_layout)

    # --- Final Setup ---
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


#red_flags_label, #scenario_label {
    color: #00FF00;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 10px;
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
        self.scenario_label.setText(f"Scenario: {challenge['scenario']}")

        # --- Red Flag Choices ---
        for i in reversed(range(self.redflags_layout.count())):
            widget = self.redflags_layout.itemAt(i).widget()
            if widget and widget != self.red_flags_label:
                widget.setParent(None)

        self.red_flag_group = QButtonGroup(self)
        for flag in challenge['red_flags']:
            btn = QRadioButton(flag)
            btn.setToolTip(challenge.get('red_flags_info', {}).get(flag, ''))
            self.red_flag_group.addButton(btn)
            self.redflags_layout.addWidget(btn)

        # --- Response Choices ---
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

        # --- Tools ---
        for i in reversed(range(self.tools_layout.count())):
            widget = self.tools_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for tool in challenge.get("tools", []):
            tool_button = QPushButton(tool)
            tool_button.setToolTip(challenge.get('tools_info', {}).get(tool, ''))
            tool_button.clicked.connect(lambda _, t=tool: self.use_tool(t))
            self.tools_layout.addWidget(tool_button)

        self.update_info()

    def check_response(self):
        selected_flag_btn = self.red_flag_group.checkedButton()
        selected_response_btn = self.response_group.checkedButton()

        if not selected_flag_btn or not selected_response_btn:
            QMessageBox.warning(self, "Warning", "Please select a red flag and a response.")
            return

        selected_flag = selected_flag_btn.text()
        selected_response = selected_response_btn.text()

        challenge = self.challenges[self.current_index]

        correct_flag = challenge['correct_flags'][0]  # support for one correct flag for now
        correct_response = challenge['correct_response']

        if selected_flag == correct_flag and selected_response == correct_response:
            selected_flag_btn.setStyleSheet("background-color: #00FF00; color: black; border: 2px solid #00FF00;")
            selected_response_btn.setStyleSheet("background-color: #00FF00; color: black; border: 2px solid #00FF00;")
            self.score += challenge['score']
            self.play_sound("correct")
            QMessageBox.information(self, "Correct", "Good job! That's the correct red flag and response.")
        else:
            if selected_flag != correct_flag:
                selected_flag_btn.setStyleSheet("background-color: #FF0000; color: white; border: 2px solid #FF0000;")
            if selected_response != correct_response:
                selected_response_btn.setStyleSheet("background-color: #FF0000; color: white; border: 2px solid #FF0000;")

            self.play_sound("incorrect")
            QMessageBox.critical(self, "Incorrect", f"Correct Red Flag: {correct_flag}\nCorrect Response: {correct_response}", buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)

        self.current_index += 1
        self.time_left = 60  # Reset timer
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

    def use_tool(self, tool_name):
     if self.tool_used:
      QMessageBox.information(self, "Limit Reached", "You can only use one tool per challenge.")
     return
    def use_tool(self, tool_name):
     if hasattr(self, "tool_used") and self.tool_used:
        QMessageBox.information(self, "Limit Reached", "You can only use one tool per challenge.")
        return

     self.tool_used = True  # Mark tool as used

     challenge = self.challenges[self.current_index]

     if tool_name == "HINT":
        hint = f"Think about: {', '.join(challenge['correct_flags'])}"
        QMessageBox.information(self, "Hint", hint)

     elif tool_name in ["VERIFY CALLER", "PHONE VERIFY"]:
        QMessageBox.information(self, "Tool Used", "You tried to verify the caller’s identity. Good step.")

     elif tool_name in ["POLICY CHECK", "FINANCE POLICY"]:
        QMessageBox.information(self, "Tool Used", challenge['policy_reminder'])

     elif tool_name == "IT DIRECTORY":
        QMessageBox.information(self, "Tool Used", "Checked IT directory. No such request from IT.")

     elif tool_name == "EMAIL HEADER CHECK":
        QMessageBox.information(self, "Tool Used", "Header shows spoofed email domain.")

     elif tool_name == "SECURITY PORTAL":
        QMessageBox.information(self, "Tool Used", "The portal confirms no reset request was initiated.")

     else:
        QMessageBox.information(self, "Tool Used", f"{tool_name} used. No suspicious activity found.")

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time Left: {self.time_left} sec")

        if self.time_left == 0:
            QMessageBox.warning(self, "Time's Up", "You ran out of time for this challenge!")
            self.current_index += 1
            self.time_left = 60  # Reset timer for next challenge
            self.load_challenge()

    def close_game(self):
        response = QMessageBox.question(self, "Exit Game", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            self.close()

    def prevent_screenshot(self):
        hwnd = int(self.winId())
        try:
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 1)  # WDA_MONITOR
        except Exception as e:
            print(f"Screenshot protection not supported: {e}")
    