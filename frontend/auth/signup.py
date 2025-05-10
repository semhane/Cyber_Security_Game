import sys
import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.fonts=false"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.routes.auth import signup_user
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QFrame, QSizePolicy, QHBoxLayout,
    QMainWindow, QMessageBox
)
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor
from PyQt5.QtCore import Qt
from backend.supabase_client import supabase


class CyberDefendApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CyberDefend - SignUp")
        self.setFixedSize(1000, 700)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Initialize departments dictionary - will be populated from database
        self.departments = {}
        
        # Dark Theme Palette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))
        self.setPalette(palette)

        # Title Bar
        self.create_title_bar()
        
        # UI
        self.setStyleSheet("background-color: black;")
        self.init_ui()
        
        # Load departments from database
        self.load_departments()

    def load_departments(self):
        try:
            # For debugging
            print("Loading departments...")
            
            # Fetch departments from the database - using correct column names
            departments_response = supabase.table("departments").select("department_id, department_name").execute()
            
            # Print response for debugging
            print(f"Departments response: {departments_response}")
            
            # Check if we have data
            if hasattr(departments_response, 'data') and departments_response.data:
                # Clear existing items
                self.department_combo.clear()
                
                # Store department data for later reference - using correct column names
                self.departments = {}
                for dept in departments_response.data:
                    # Clean up department names (remove any trailing whitespace)
                    clean_name = dept["department_name"].strip()
                    self.departments[clean_name] = dept["department_id"]
                
                # Add department names to combobox
                self.department_combo.addItems(self.departments.keys())
                print(f"Added {len(self.departments)} departments to dropdown: {list(self.departments.keys())}")
            else:
                print("No departments found in response")
                # Don't use fallback departments anymore
        except Exception as e:
            print(f"Exception while loading departments: {str(e)}")
            # Don't use fallback departments anymore

    def register_user(self, username, email, password, department_name):
        # Clear previous status messages
        if hasattr(self, 'status_label'):
            self.status_label.setText("")
        
        # Get the department ID based on the selected name
        department_id = self.departments.get(department_name)
        
        # Form validation
        if not all([username, email, password]):
            self.show_status("All fields are required!", is_error=True)
            return
        
        # Make sure department is valid
        if department_name not in self.departments:
            self.show_status("Invalid department selected!", is_error=True)
            return
            
        # Get department ID
        department_id = self.departments[department_name]
        print(f"Selected department: {department_name}, ID: {department_id}")
            
        result = signup_user(
            username=username,
            email=email,
            password=password,
            department_name=department_name,
            score=0
        )

        if result.get("success"):
            # Show success message box with green styling
            success_msg = QMessageBox(self)
            success_msg.setWindowTitle("Registration Success")
            success_msg.setText("SIGNUP SUCCESSFUL!")
            success_msg.setInformativeText("Welcome to CyberDefend Training Protocol")
            success_msg.setIcon(QMessageBox.Information)
            
            # Apply custom styling to the message box
            success_msg.setStyleSheet("""
                QMessageBox {
                    background-color: black;
                }
                QLabel {
                    color: #00FF00;
                    font-family: 'Courier';
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: #003300;
                    color: #00FF00;
                    border: 1px solid #00FF00;
                    padding: 5px 10px;
                    font-family: 'Courier';
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #00FF00;
                    color: black;
                }
            """)
            
            # Show the message box
            success_msg.exec_()
            
            # Also show the status message in the form
            self.show_status("Registration successful! Initializing training protocol...", is_error=False)
            
            # Open dashboard after successful registration
            self.open_dashboard()
        else:
            self.show_status(result.get("message"), is_error=True)

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

    def create_title_bar(self):
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #282828;")
        title_bar_layout = QHBoxLayout()
        title_bar.setLayout(title_bar_layout)

        # Dots on the left
        dots_container = QWidget()
        dots_layout = QHBoxLayout(dots_container)
        dots_layout.setSpacing(8)
        dots_layout.setContentsMargins(15, 0, 0, 0)

        for color in ["#FF5F56", "#FFBD2E", "#27C93F"]:
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            dots_layout.addWidget(dot)

        title_bar_layout.addWidget(dots_container)

        # Centered Title
        title_label = QLabel("CYBERDEFEND PROTOCOL v2.7.1")
        title_label.setFont(QFont("Consolas", 10, QFont.Bold))
        title_label.setStyleSheet("color: #00ff00;")
        title_label.setAlignment(Qt.AlignCenter)

        title_container = QWidget()
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        title_container_layout.addWidget(title_label)
        title_bar_layout.addWidget(title_container, 1)

        self.setMenuWidget(title_bar)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def resizeEvent(self, event):
        if hasattr(self, 'box_frame'):
            self.box_frame.setFixedWidth(int(self.width() * 0.5))

    def init_ui(self):
        green = "#00FF00"
        darker_green = "#003300"

        # Custom Title and Subtitle
        title_label = QLabel("CYBERDEFEND")
        title_label.setFont(QFont("Arial", 38, QFont.Bold))
        title_label.setStyleSheet(f"color: {green};")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("SECURITY AWARENESS TRAINING")
        subtitle.setFont(QFont("Courier", 24, QFont.Normal))
        subtitle.setStyleSheet(f"color: {green};")
        subtitle.setAlignment(Qt.AlignCenter)

        # Registration Box
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
        input_style = f"""
            color: {green};
            background-color: black;
            border: 1px solid {green};
            padding: 4px;
            font-size: 14px;
        """

        def add_field(layout, label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet(label_style)
            label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            layout.addWidget(label)
            layout.addWidget(widget)

        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(10)

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(25)
        self.username_input.setStyleSheet(input_style)

        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(25)
        self.email_input.setStyleSheet(input_style)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(25)
        self.password_input.setStyleSheet(input_style)

        self.department_combo = QComboBox()
        self.department_combo.setFixedHeight(25)
        self.department_combo.setStyleSheet(input_style)
        # Departments will be loaded from database in load_departments method

        add_field(self.form_layout, "USERNAME:", self.username_input)
        add_field(self.form_layout, "EMAIL:", self.email_input)
        add_field(self.form_layout, "PASSWORD:", self.password_input)
        add_field(self.form_layout, "DEPARTMENT:", self.department_combo)

        box_layout.addLayout(self.form_layout)
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
                cursor: pointer;
            }}
        """)
        # Set cursor to pointing hand when hovering
        init_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        init_btn.clicked.connect(lambda: self.register_user(
            self.username_input.text(),
            self.email_input.text(),
            self.password_input.text(),
            self.department_combo.currentText()
        ))
        box_layout.addWidget(init_btn)

        login_label = QLabel("<a href='#' style='text-decoration: none; color: #00FF00;'>Already have an account?</a>")
        login_label.setStyleSheet(f"color: {green}; font: bold 12pt Courier; border: none; background-color: transparent;")
        login_label.setAlignment(Qt.AlignRight)
        login_label.setOpenExternalLinks(False)  # Set to False so we can handle the link ourselves
        login_label.linkActivated.connect(self.open_login_page)
        login_label.setCursor(QCursor(Qt.PointingHandCursor))  # Change cursor for login link too
        box_layout.addWidget(login_label)
        box_layout.addSpacing(10)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title_label)
        center_layout.addWidget(subtitle)
        center_layout.addSpacing(20)
        center_layout.addWidget(self.box_frame)

        central_widget = QWidget()
        outer_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        outer_layout.addStretch()
        outer_layout.addLayout(center_layout)
        outer_layout.addStretch()

    def open_login_page(self):
        print("Opening login page...")
        self.close()
        from login import CyberDefendLoginApp
        self.login_window = CyberDefendLoginApp()
        self.login_window.show()
        
def open_dashboard(self):
    print("Opening dashboard...")
    self.close()
    
    # Approach 1: If dashboard_window.py is in a directory outside the auth directory
    # This uses a direct import assuming dashboard_window.py is in a parent directory
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from frontend.dashboard.dashboard_window import CyberDefendDashboardApp
    
    # Alternative approach 2: If dashboard_window.py is in the same directory as login.py
    # Uncomment this and comment out the above if needed
    # from dashboard_window import CyberDefendDashboardApp
    
    # Create the dashboard and pass the current user data
    self.dashboard_window = CyberDefendDashboardApp(user_data=getattr(self, 'current_user', None))
    self.dashboard_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CyberDefendApp()
    win.show()
    sys.exit(app.exec_())