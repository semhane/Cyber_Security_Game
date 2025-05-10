import sys
import os
import bcrypt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.supabase_client import supabase

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QSizePolicy, QHBoxLayout, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor
from PyQt5.QtCore import Qt, QTimer


class CyberDefendLoginApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CyberDefend - Login")
        self.setFixedSize(1000, 700)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # User data placeholder
        self.current_user = None

        # Set dark theme palette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))
        self.setPalette(palette)

        # UI
        self.setStyleSheet("background-color: black;")

        # Create the custom title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #282828;")
        title_bar_layout = QHBoxLayout()
        title_bar.setLayout(title_bar_layout)

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
        
        # Create a container for proper centering
        title_container = QWidget()
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        title_container_layout.addWidget(title_label)
        
        # Add the title container with stretch factors for perfect centering
        title_bar_layout.addWidget(title_container, 1)  # Takes all available space
        
        # Set this as the menu bar (acts as title bar)
        self.setMenuWidget(title_bar)
        
        # Create central widget for the login content
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.init_ui(central_widget)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def show_status(self, message, is_error=False):
        if not hasattr(self, 'status_label'):
            self.status_label = QLabel()
            self.status_label.setAlignment(Qt.AlignCenter)
            self.status_label.setFont(QFont("Courier", 10))
            self.form_layout.addWidget(self.status_label)
        
        if is_error:
            self.status_label.setStyleSheet("color: red; background-color: #330000; padding: 5px; border: 1px solid red;")
        else:
            self.status_label.setStyleSheet("color: #00ff00; background-color: #003300; padding: 5px; border: 1px solid #00ff00;")
        
        self.status_label.setText(message)

    def authenticate_user(self, username_or_email, password):
        try:
            # Check if input is empty
            if not username_or_email or not password:
                self.show_status("Please enter both username/email and password", is_error=True)
                return False

            # Try to find user by email first
            user_response = supabase.table("users").select("*").eq("email", username_or_email).execute()
            
            # If no user found by email, try username
            if not user_response.data:
                user_response = supabase.table("users").select("*").eq("username", username_or_email).execute()
                
            # If still no user found
            if not user_response.data:
                self.show_status("User does not exist", is_error=True)
                return False
                
            user = user_response.data[0]
            
            # Verify password using bcrypt
            stored_hash = user["password_hash"]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                self.show_status("Login successful!", is_error=False)
                # Store user info for the dashboard
                self.current_user = user
                return True
            else:
                self.show_status("Incorrect password", is_error=True)
                return False
                
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            self.show_status(f"Login error: {str(e)}", is_error=True)
            return False

    def open_signup_page(self):
        print("Opening signup page...")
        self.close()
        from signup import CyberDefendApp
        self.signup_window = CyberDefendApp()
        self.signup_window.show()
    
    def open_dashboard(self):
        print("Opening dashboard...")
        self.close()
        
        # Get the absolute path to the dashboard directory
        dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dashboard'))
        sys.path.append(dashboard_path)
        
        # Try different import methods and class names
        # Method 1: Try importing directly
        try:
            from dashboard_window import CyberDefendDashboardApp
            self.dashboard_window = CyberDefendDashboardApp(user_id=self.current_user["id"])
            self.dashboard_window.show()
            return
        except (ModuleNotFoundError, ImportError) as e:
            print(f"Import error 1: {str(e)}")
        
        try:
            from dashboard.dashboard_window import CyberDefendDashboardApp
            self.dashboard_window = CyberDefendDashboardApp(user_id=self.current_user["id"])
            self.dashboard_window.show()
            return
        except (ModuleNotFoundError, ImportError) as e:
            print(f"Import error 2: {str(e)}")
            
        # Method 2: Try importing from the parent directory
        try:
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
            from dashboard.dashboard_window import DashboardApp
            self.dashboard_window = CyberDefendDashboardApp(user_id=self.current_user["id"])
            self.dashboard_window.show()
            return
        except (ModuleNotFoundError, ImportError) as e:
            print(f"Import error 3: {str(e)}")
        
        # Method 3: Look for main.py in dashboard
        try:
            from main import DashboardApp
            self.dashboard_window = CyberDefendDashboardApp(user_id=self.current_user["id"])
            self.dashboard_window.show()
            return
        except (ModuleNotFoundError, ImportError) as e:
            print(f"Import error 4: {str(e)}")
            
        # If all import attempts fail, create a placeholder message
        QMessageBox.warning(
            self, 
            "Dashboard Import Error", 
            "Could not find the dashboard module. Please check your file structure and ensure the dashboard module exists."
        )
        print(f"Could not find dashboard module. Paths tried: {dashboard_path}, {os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))}")

    def show_password_reset_dialog(self):
        email, ok = QInputDialog.getText(self, "Reset Password", "Enter your email address:")
        if ok and email:
            # Check if email exists in the system
            user_response = supabase.table("users").select("*").eq("email", email).execute()
            
            if not user_response.data:
                self.show_status("Email not found in system", is_error=True)
                return
                
            # In a real app, you would send a password reset email here
            # For now, we'll just show a success message
            QMessageBox.information(self, "Password Reset", 
                                   "If your email is registered in our system, you will receive a password reset link shortly.")

    def init_ui(self, central_widget):
        # Define colors
        green = "#00FF00"
        darker_green = "#003300"

        # Main Title
        title_label = QLabel("CYBERDEFEND")
        title_font = QFont("Arial", 38, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {green};")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("SECURITY AWARENESS TRAINING")
        subtitle_font = QFont("Courier", 24, QFont.Normal)  # Adjusted size for better fit
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
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setContentsMargins(20, 20, 20, 20)

        # Input fields
        self.username_or_email_input = QLineEdit()
        self.username_or_email_input.setStyleSheet(input_style)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        add_field(self.form_layout, "EMAIL/USERNAME:", self.username_or_email_input)
        add_field(self.form_layout, "PASSWORD:", self.password_input)

        # Links container
        links_layout = QHBoxLayout()
        
        # Sign Up link on the left
        signup_label = QLabel("<a href='#' style='text-decoration: none; color: #00FF00; background-color: transparent;'>Sign Up</a>")
        signup_label.setStyleSheet(f"color: {green}; font: bold 12pt Courier; border: none;")
        signup_label.setOpenExternalLinks(False)  # Handle the link ourselves
        signup_label.linkActivated.connect(self.open_signup_page)
        signup_label.setCursor(QCursor(Qt.PointingHandCursor))  # Change cursor for sign up link
        links_layout.addWidget(signup_label)
        
        # Spacer to push Forgot Password to the right
        links_layout.addStretch()
        
        # Forgot Password link on the right
        forgot_password_label = QLabel("<a href='#' style='text-decoration: none; color: #00FF00; background-color: transparent;'>Forgot Password?</a>")
        forgot_password_label.setStyleSheet(f"color: {green}; font: bold 12pt Courier; border: none;")
        forgot_password_label.setOpenExternalLinks(False)  # Handle the link ourselves
        forgot_password_label.linkActivated.connect(self.show_password_reset_dialog)
        forgot_password_label.setCursor(QCursor(Qt.PointingHandCursor))  # Change cursor for forgot password link
        links_layout.addWidget(forgot_password_label)
        
        self.form_layout.addLayout(links_layout)

        box_layout.addLayout(self.form_layout)

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
        # Set cursor to pointing hand when hovering
        login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Connect login button to authentication logic
        login_btn.clicked.connect(lambda: self.process_login())
        box_layout.addWidget(login_btn)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title_label)
        center_layout.addWidget(subtitle)
        center_layout.addSpacing(20)
        center_layout.addWidget(self.box_frame)

        # Outer layout
        outer_layout = QVBoxLayout(central_widget)
        outer_layout.addStretch()
        outer_layout.addLayout(center_layout)
        outer_layout.addStretch()

    def process_login(self):
        username_or_email = self.username_or_email_input.text()
        password = self.password_input.text()
        
        if self.authenticate_user(username_or_email, password):
            # Pause briefly to show the success message before transitioning
            QTimer.singleShot(1000, self.open_dashboard)
    
    @property
    def user_id(self):
        """Return the authenticated user ID"""
        if self.current_user and 'id' in self.current_user:
            return self.current_user['id']
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberDefendLoginApp()
    window.show()
    sys.exit(app.exec_())