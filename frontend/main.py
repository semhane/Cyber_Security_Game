# frontend/main.py

import sys
from PyQt5.QtWidgets import QApplication
# from games.social_engineering.social_engineering import GameWindow
# from games.social_engineering.social_engineering_data import CHALLENGES
from games.general_qcm.general_qcm import GameWindow
from games.general_qcm.general_qcm_data import CHALLENGES
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Gamer info — shown in top-right of the game window
    gamer_info = {
        "name": "Alice",
        "department": "Cybersecurity Dept."
    }

    window = GameWindow(CHALLENGES, gamer_info)
    window.show()
    sys.exit(app.exec_())
