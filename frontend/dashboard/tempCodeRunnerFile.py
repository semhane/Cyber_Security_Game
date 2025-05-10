import sys
import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts=false"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.supabase_client import supabase

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout, QButtonGroup, QSizePolicy, QMainWindow
)
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor
from PyQt5.QtCore import Qt

class CyberDefendDashboardApp(QMainWindow): 
    def __init__(self, user_id=None, user_data=None):
        super().__init__()
        self.setWindowTitle("CyberDefend - Dashboard")
        self.setFixedSize(1000, 700)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Store user data if provided, otherwise we'll fetch it later
        self.user_data = user_data
        self.user_id = user_id
        
        # Set dark theme palette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))
        self.setPalette(palette)

        # Create the custom title bar
        self.create_title_bar()
        
        # Load user data if needed
        if self.user_data is None:
            self.load_user_data_from_supabase()
        
        # Add the rest of the UI
        self.init_ui()

    def load_user_data_from_supabase(self):
        """Load user data from Supabase including department name, XP, and unlocked games"""
        try:
            # If user_id is provided, fetch that specific user
            if self.user_id:
                user_query = supabase.table("users").select("*").eq("id", self.user_id)
            else:
                # Otherwise get the most recently added user for demo purposes
                user_query = supabase.table("users").select("*").order("created_at", desc=True).limit(1)
            
            user_result = user_query.execute()
            
            if user_result.data:
                self.user_data = user_result.data[0]
                
                # Get department name from departments table
                if self.user_data.get("department_id"):
                    try:
                        dept_result = supabase.table("departments").select("department_name").eq("id", self.user_data["department_id"]).execute()
                        if dept_result.data and len(dept_result.data) > 0:
                            self.user_data["department"] = dept_result.data[0]["department_name"]
                        else:
                            print("Department not found in database, using default")
                            self.user_data["department"] = "IT"  # Default if not found
                    except Exception as e:
                        print(f"Error fetching department: {str(e)}")
                        self.user_data["department"] = "IT"  # Default on error
                else:
                    self.user_data["department"] = "IT"  # Default if no department_id
                
                # Get total XP as sum of all scores from user_game_logs
                logs_result = supabase.table("user_game_logs").select("score").eq("user_id", self.user_data["id"]).execute()
                if logs_result.data:
                    total_xp = sum(log["score"] for log in logs_result.data if "score" in log)
                    self.user_data["total_xp"] = total_xp
                else:
                    self.user_data["total_xp"] = 0
                
                # Get game data to determine which games should be unlocked
                games_result = supabase.table("games").select("*").order("id").execute()
                games = games_result.data if games_result.data else []
                
                # Default games dictionary in case of no games found
                default_games = {
                    1: {"name": "general_qcm", "min_score": 0},
                    2: {"name": "password_strength", "min_score": 100},
                    3: {"name": "phishing_quiz", "min_score": 200},
                    4: {"name": "social_engineering", "min_score": 300}
                }
                
                # Convert games list to dictionary for easier access
                games_dict = {}
                if games:
                    for game in games:
                        game_id = game.get("id")
                        if game_id:
                            games_dict[game_id] = {
                                "name": game.get("name"),
                                "min_score": game.get("min_score", 0)
                            }
                else:
                    games_dict = default_games
                
                # Determine which games should be unlocked based on total XP
                total_xp = self.user_data["total_xp"]
                unlocked_games = []
                
                for game_id, game_info in games_dict.items():
                    if total_xp >= game_info.get("min_score", 0):
                        unlocked_games.append(game_id)
                
                # Ensure at least the first game is unlocked
                general_qcm_id = self.get_general_qcm_id()
                if general_qcm_id not in unlocked_games:
                    unlocked_games.append(general_qcm_id)
                
                self.user_data["unlocked_games"] = unlocked_games
                
                # Debug print
                print(f"User: {self.user_data.get('username')}")
                print(f"Department: {self.user_data.get('department')}")
                print(f"Total XP: {self.user_data.get('total_xp')}")
                print(f"Unlocked Games: {self.user_data.get('unlocked_games')}")
                
            else:
                # Create default user data if no user found
                self.user_data = {
                    "id": 1,
                    "username": "DEFENDER",
                    "department": "IT",
                    "total_xp": 0,
                    "unlocked_games": [self.get_general_qcm_id()]  # Only first game unlocked
                }
        except Exception as e:
            print(f"Error loading user data: {str(e)}")
            # Default user data
            self.user_data = {
                "id": 1,
                "username": "DEFENDER",
                "department": "IT",
                "total_xp": 0,
                "unlocked_games": [self.get_general_qcm_id()]  # Only first game unlocked
            }

    def get_general_qcm_id(self):
        """Get the ID of the general_qcm game from the database"""
        try:
            result = supabase.table("games").select("id").eq("name", "general_qcm").execute()
            if result.data and len(result.data) > 0:
                return result.data[0]["id"]
            return 1  # Default ID if not found
        except Exception as e:
            print(f"Error getting general_qcm ID: {str(e)}")
            return 1  # Default ID if error
    
    def calculate_rank(self, xp):
        """Calculate security rank based on XP using updated thresholds"""
        if xp < 200:
            return "BEGINNER"
        elif xp < 400:
            return "INTERMEDIATE"
        else:
            return "ADVANCED"

    def is_game_unlocked(self, game_id):
        """Check if a game is unlocked for the user"""
        unlocked_games = self.user_data.get("unlocked_games", [])
        return game_id in unlocked_games

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def create_title_bar(self):
        title_bar = QWidget()
        title_bar.setFixedHeight(35)
        title_bar.setStyleSheet("background-color: #282828;")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

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
        title_container = QWidget()
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        title_container_layout.addWidget(title_label)
        title_bar_layout.addWidget(title_container, 1)

        # Set as menu widget (title bar)
        self.setMenuWidget(title_bar)

    def start_game(self, game_name):
        """Start the selected game"""
        try:
            if game_name == "general_qcm":
                from games.general_qcm.challenge_one import GameWindow
                self.game_window = GameWindow(self.user_data["id"])
                self.game_window.show()
                self.close()
            elif game_name == "password_strength":
                from games.password_strength.challenge_one import GameWindow
                self.game_window = GameWindow(self.user_data["id"])
                self.game_window.show()
                self.close()
            elif game_name == "phishing_quiz":
                from games.phishing_quiz.challenge_one import GameWindow
                self.game_window = GameWindow(self.user_data["id"])
                self.game_window.show()
                self.close()
            elif game_name == "social_engineering":
                from games.social_engineering.challenge_one import GameWindow
                self.game_window = GameWindow(self.user_data["id"])
                self.game_window.show()
                self.close()
        except Exception as e:
            print(f"Error starting game {game_name}: {str(e)}")

    def init_ui(self):
        green = "#00FF00"
        darker_green = "#003300"
        gray = "#666666"
        red = "#FF0000"
        dark_gray = "#1a1a1a"

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        def styled_label(text, font_size=12, bold=False, align=Qt.AlignLeft, color=green):
            label = QLabel(text)
            font = QFont("Courier", font_size)
            font.setBold(bold)
            label.setFont(font)
            label.setStyleSheet(f"color: {color}; padding: 5px;")
            label.setAlignment(align)
            return label

        title = styled_label("CYBERDEFEND", 70, True, Qt.AlignCenter)
        subtitle = styled_label("SECURITY AWARENESS TRAINING", 10, False, Qt.AlignCenter)

        # Get username and department from user data
        username = self.user_data.get("username", "DEFENDER").upper()
        department = self.user_data.get("department", "IT").upper()
        
        # Get total XP and calculate rank
        total_xp = self.user_data.get("total_xp", 0)
        security_rank = self.calculate_rank(total_xp)
        
        # Add rank emoji based on level
        rank_emoji = "🔰" if security_rank == "BEGINNER" else "🎉" if security_rank == "INTERMEDIATE" else "🏆"

        # Update left info with actual username and department
        left_info_text = QLabel(f"AGENT: {username}\nDEPARTMENT: {department}")
        left_info_text.setFont(QFont("Courier", 12))
        left_info_text.setStyleSheet(f"color: {green}; border: none;")
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
        left_info_layout.addWidget(left_info_text)

        # Update right info with actual rank and XP
        right_info_text = QLabel(f"RANK: {rank_emoji} {security_rank}\nXP: {total_xp}/400")
        right_info_text.setFont(QFont("Courier", 12))
        right_info_text.setStyleSheet(f"color: {green}; border: none;")
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
        right_info_layout.addWidget(right_info_text)

        central_container = QWidget()
        central_layout = QVBoxLayout(central_container)
        central_layout.addWidget(title)
        central_layout.addWidget(subtitle)
        central_layout.setAlignment(Qt.AlignCenter)

        top_horizontal_container = QWidget()
        top_horizontal_layout = QHBoxLayout(top_horizontal_container)
        top_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        top_horizontal_layout.setSpacing(50)
        top_horizontal_layout.addWidget(left_info_frame, alignment=Qt.AlignLeft)
        top_horizontal_layout.addWidget(central_container, alignment=Qt.AlignCenter)
        top_horizontal_layout.addWidget(right_info_frame, alignment=Qt.AlignRight)

        self.main_layout.addWidget(top_horizontal_container)

        mission_title = QLabel("MISSION SELECTION")
        mission_title.setFont(QFont("Courier", 16, QFont.Bold))
        mission_title.setStyleSheet(f"""
            color: {green};
            background-color: {dark_gray};
            padding: 12px;
            border-radius: 0px;
        """)
        mission_title.setAlignment(Qt.AlignCenter)

        mission_grid = QGridLayout()
        mission_grid.setContentsMargins(10, 10, 10, 10)
        mission_grid.setSpacing(10)

        def create_mission_box(title, desc, game_name, game_id, special=False):
            # Check if this game is unlocked for the user
            is_unlocked = self.is_game_unlocked(game_id)
            color = red if not is_unlocked else green
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    border: 1px solid {color};
                    padding: 10px;
                    border-radius: 8px;
                    background-color: {dark_gray};
                }}
            """)
            layout = QVBoxLayout(frame)
            title_label = QLabel(title)
            title_font = QFont("Courier", 14)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet(f"color: {color}; border:none;")
            layout.addWidget(title_label)

            desc_label = QLabel(desc)
            desc_label.setFont(QFont("Courier", 11))
            desc_label.setStyleSheet(f"color: {color}; border:none;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

            button = QPushButton("LOCKED" if not is_unlocked else "START")
            button.setEnabled(is_unlocked)
            button.setFont(QFont("Courier", 11))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {color};
                    border: 1px solid {color};
                    padding: 6px;
                }}
                QPushButton:disabled {{
                    color: {red};
                    border: 1px solid {red};
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: black;
                    cursor: pointer;
                }}
            """)
            if is_unlocked:
                button.setCursor(QCursor(Qt.PointingHandCursor))
                button.clicked.connect(lambda: self.start_game(game_name))
            layout.addWidget(button, alignment=Qt.AlignRight)
            return frame

        # Get game data from DB
        try:
            games_result = supabase.table("games").select("*").execute()
            
            if games_result.data:
                # Create a dictionary of games by name for easier access
                game_data = {}
                for game in games_result.data:
                    game_data[game.get("name")] = {
                        "id": game.get("id"),
                        "name": game.get("name"),
                        "description": game.get("description", "No description"),
                        "min_score": game.get("min_score", 0)
                    }
            else:
                # Default games in case no games found
                game_data = {
                    "general_qcm": {"id": 1, "name": "general_qcm", "description": "Learn and test your general cybersecurity knowledge.", "min_score": 0},
                    "password_strength": {"id": 2, "name": "password_strength", "description": "Create strong passwords and avoid common password vulnerabilities.", "min_score": 100},
                    "phishing_quiz": {"id": 3, "name": "phishing_quiz", "description": "Learn to identify and respond to common phishing attempts.", "min_score": 200},
                    "social_engineering": {"id": 4, "name": "social_engineering", "description": "Detect and counter social engineering attacks.", "min_score": 300}
                }
        except Exception as e:
            print(f"Error loading games: {str(e)}")
            # Default games in case of error
            game_data = {
                "general_qcm": {"id": 1, "name": "general_qcm", "description": "Learn and test your general cybersecurity knowledge.", "min_score": 0},
                "password_strength": {"id": 2, "name": "password_strength", "description": "Create strong passwords and avoid common password vulnerabilities.", "min_score": 100},
                "phishing_quiz": {"id": 3, "name": "phishing_quiz", "description": "Learn to identify and respond to common phishing attempts.", "min_score": 200},
                "social_engineering": {"id": 4, "name": "social_engineering", "description": "Detect and counter social engineering attacks.", "min_score": 300}
            }

        # Add all game boxes to the grid
        if "general_qcm" in game_data:
            mission_grid.addWidget(create_mission_box(
                "LEVEL 1: CYBERSECURITY BASICS",
                game_data["general_qcm"].get("description", "Learn cybersecurity basics."),
                "general_qcm",
                game_data["general_qcm"].get("id", 1)
            ), 0, 0)
        else:
            # Fallback if general_qcm not found
            mission_grid.addWidget(create_mission_box(
                "LEVEL 1: CYBERSECURITY BASICS",
                "Learn and test your general cybersecurity knowledge.",
                "general_qcm", 1
            ), 0, 0)
        
        if "password_strength" in game_data:
            mission_grid.addWidget(create_mission_box(
                "LEVEL 2: PASSWORD SECURITY",
                game_data["password_strength"].get("description", "Create strong passwords and avoid common password vulnerabilities."),
                "password_strength",
                game_data["password_strength"].get("id", 2)
            ), 0, 1)
        else:
            # Fallback if password_strength not found
            mission_grid.addWidget(create_mission_box(
                "LEVEL 2: PASSWORD SECURITY",
                "Create strong passwords and avoid common password vulnerabilities.",
                "password_strength", 2
            ), 0, 1)
        
        if "phishing_quiz" in game_data:
            mission_grid.addWidget(create_mission_box(
                "LEVEL 3: PHISHING DEFENSE",
                game_data["phishing_quiz"].get("description", "Learn to identify and respond to common phishing attempts."),
                "phishing_quiz",
                game_data["phishing_quiz"].get("id", 3)
            ), 1, 0)
        else:
            # Fallback if phishing_quiz not found
            mission_grid.addWidget(create_mission_box(
                "LEVEL 3: PHISHING DEFENSE",
                "Learn to identify and respond to common phishing attempts.",
                "phishing_quiz", 3
            ), 1, 0)
        
        if "social_engineering" in game_data:
            mission_grid.addWidget(create_mission_box(
                "LEVEL 4: SOCIAL ENGINEERING",
                game_data["social_engineering"].get("description", "Detect and counter social engineering attacks."),
                "social_engineering",
                game_data["social_engineering"].get("id", 4)
            ), 1, 1)
        else:
            # Fallback if social_engineering not found
            mission_grid.addWidget(create_mission_box(
                "LEVEL 4: SOCIAL ENGINEERING",
                "Detect and counter social engineering attacks.",
                "social_engineering", 4
            ), 1, 1)

        box_frame = QFrame()
        box_frame.setStyleSheet(f"""
            QFrame {{
                border: 1px solid {green};  
                border-radius: 10px;
                background-color: black;
            }}
        """)
        box_layout = QVBoxLayout(box_frame)
        box_layout.setContentsMargins(5, 5, 5, 5)
        box_layout.addWidget(mission_title)
        box_layout.addLayout(mission_grid)

        self.main_layout.addWidget(box_frame)
        self.main_layout.addStretch()


# Example for direct testing of the dashboard
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # For direct testing, you can create a dummy user or load a real one
    # In practice, this user_id would come from your login system
    user_id = None  # Set this to a valid user ID to test with a specific user
    
    # Alternatively, you can pass in user data directly
    dummy_user = {
        "id": user_id,
        "username": "TEST_USER",
        "department": "SECURITY",
        "total_xp": 250,  # Will show as INTERMEDIATE
        "unlocked_games": [1, 2, 3]  # Has first three games unlocked
    }
    
    # You can pass user_id, user_data, or neither (will load most recent user)
    window = CyberDefendDashboardApp(user_id=user_id)  # Or pass user_data=dummy_user
    window.show()
    sys.exit(app.exec_())