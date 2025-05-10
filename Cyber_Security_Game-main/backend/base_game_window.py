from PyQt5.QtWidgets import QWidget, QButtonGroup, QRadioButton, QMessageBox
# backend.py

from PyQt5.QtWidgets import QWidget, QButtonGroup, QRadioButton, QMessageBox
from PyQt5.QtCore import QTimer
import winsound
import ctypes
from game_logic import submit_qcm_result
from game_logic import update_user_score
class BaseGameWindow(QWidget):
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

    
    def check_response(self):
        pass

    def show_summary(self):
        self.timer.stop()
        self.hide()  # Hide the game window

        # Submit the final results to backend
        submit_qcm_result(self.gamer_info['id'], self.score)
        update_user_score(self.gamer_info['id'], self.score)

        # Show a final score message
        final_message = QMessageBox()
        final_message.setWindowTitle("Game Over")
        final_message.setText(f"🎯 Game Over!\n\n🏆 Your Score: {self.score}\n🔰 Experience Gained: {self.score * 10}")
        final_message.setStandardButtons(QMessageBox.Ok)
        final_message.setIcon(QMessageBox.Information)
        final_message.exec_()

        self.close()  # Close the game after showing summary
    def update_score_and_experience(self, new_score, new_experience):
        self.score = new_score
        self.experience = new_experience
        self.score_label.setText(f"Score: {self.score}")
        self.experience_label.setText(f"Experience: {self.experience}")


    def play_sound(self, result_type):
        if not self.sound_on:
            return
        if result_type == "correct":
            winsound.Beep(1000, 200)  # Higher beep for correct
        elif result_type == "incorrect":
            winsound.Beep(400, 400)  # Lower beep for incorrect

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.sound_toggle.setText("🔊 ON" if self.sound_on else "🔇 OFF")

    def prevent_screenshot(self):
        # Disable screenshots using Windows API
        try:
            ctypes.windll.user32.SetWindowDisplayAffinity(int(self.winId()), 1)
        except Exception as e:
            print("Warning: Could not prevent screenshots:", e)
    
 

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(f"⏱️ {self.time_left} sec")
        else:
            # Time is over
            # Penalize: Decrease the score
            penalty_points = 5  # or whatever penalty you want
            new_score = max(self.score - penalty_points, 0)  # Avoid going negative
            new_experience = self.experience  # No experience change on timeout (unless you want)

            self.update_score_and_experience(new_score, new_experience)

            # Now check response (probably incorrect or timeout handling)
            self.check_response()
 # Automatically check (treat as no response) when time runs out

    def close_game(self):
        confirm = QMessageBox.question(self, "Exit Game", "Are you sure you want to exit?",
                                        QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.close()
    def submit_and_notify_result(self, user_id, game_id, score_earned):
        try:
            submit_qcm_result(user_id, game_id, score_earned)
            QMessageBox.information(self, "Success", "Score and experience updated successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update stats: {e}")
