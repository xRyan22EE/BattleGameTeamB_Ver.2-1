from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDesktopWidget,\
     QLabel, QLineEdit, QRadioButton, QSlider, QScrollArea

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os
import sys
import subprocess  

class FirstPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Battleship Group B")
        self.setGeometry(500, 400, 600, 600)
        self.setStyleSheet("background-color: black")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Title label
        title = QLabel("Battleship Gear B", self)
        font = QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(30)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: lightblue")

        title_layout = QHBoxLayout()
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

        layout.addLayout(title_layout)

        # Play button
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.launch_game)  # Launch the game script
        layout.addWidget(self.play_button)
        self.play_button.setStyleSheet("background-color: lightblue; border: 4px; border-radius: 9px")
        self.play_button.setCursor(Qt.PointingHandCursor)

        # Settings button
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_settings_page)  # Opens Settings page
        layout.addWidget(self.settings_button)
        self.settings_button.setStyleSheet("background-color: lightblue; border: 4px; border-radius: 9px")
        self.settings_button.setCursor(Qt.PointingHandCursor)

        # Instructions button
        self.instructions_button = QPushButton("Instructions", self)
        self.instructions_button.clicked.connect(self.open_instructions_page)  # Opens Instructions page
        layout.addWidget(self.instructions_button)
        self.instructions_button.setStyleSheet("background-color: lightblue; border: 4px; border-radius: 9px")
        self.instructions_button.setCursor(Qt.PointingHandCursor)

        # Quit button
        self.quit_button = QPushButton("Quit Game", self)
        self.quit_button.clicked.connect(self.close)  # Closes the app
        layout.addWidget(self.quit_button)
        self.quit_button.setStyleSheet("background-color: lightblue; border: 4px; border-radius: 9px")
        self.quit_button.setCursor(Qt.PointingHandCursor)

        layout.addSpacing(100)
        self.center()

    def center(self):
        """Centers the window on the screen."""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def launch_game(self):
    # Launch the game by executing Game_ver.2.7.py as a separate process
    
        try:
            script_path = os.path.join(os.path.dirname(__file__), "Game_ver.2.7.py")  # Full path
            subprocess.Popen(["python", script_path])  # Use the full path
        except Exception as e:
            print(f"Failed to launch the game: {e}")

    def open_settings_page(self):
        """Opens the settings page."""
        self.settings_page = Settings()
        self.settings_page.show()

    def open_instructions_page(self):
        """Opens the instructions page."""
        self.instructions_page = InstructionsPage()
        self.instructions_page.show()



class UsernamePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Username")
        self.setStyleSheet("background-color: black")

        # Set the geometry to match the main screen size
        self.setGeometry(500, 400, 600, 600)  # Match FirstPage size
        self.center()  # Center the window on the screen

        layout = QVBoxLayout(self)

        # Add spacing to center content vertically
        layout.addStretch(1)

        # Label for instructions
        self.label = QLabel("Enter your username:", self)
        font = QFont()
        font.setPointSize(14)
        self.label.setStyleSheet("color:lightblue")
        self.label.setFont(font)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Text box for username
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        self.username_input.setStyleSheet("color: lightblue")

        # Continue button
        self.continue_button = QPushButton("Continue", self)
        self.continue_button.clicked.connect(self.handle_continue)
        layout.addWidget(self.continue_button, alignment=Qt.AlignCenter)
        self.continue_button.setStyleSheet("background-color: lightblue; color: black")

        # Add spacing to center content vertically
        layout.addStretch(1)

        self.setLayout(layout)

    def center(self):    # Center the window on the screen
            
        screen = QDesktopWidget().screenGeometry()  # Get screen geometry
        size = self.geometry()  # Get window geometry
        x = (screen.width() - size.width()) // 2  # Calculate X position
        y = (screen.height() - size.height()) // 2  # Calculate Y position
        self.move(x, y)  # Move window to center

    def handle_continue(self):
        username = self.username_input.text()
        if username:
            print(f"Username entered: {username}")
            self.first_page = FirstPage()
            self.first_page.show()
            self.close()  # Close the username page
        else:
            self.label.setText("Please enter a username!")



class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(500, 400, 600, 600)  # Match FirstPage size
        self.center()  # Center the window on the screen
        self.setStyleSheet("background-color: black")

        # Main layout
        layout = QVBoxLayout(self)


        # Volume label
        slider = QLabel("<b>Volume:</b>", self)
        slider.setStyleSheet("color: lightblue")
        slider.setAlignment(Qt.AlignCenter)
        layout.addWidget(slider)

        # Slider for volume control
        sldr1 = QSlider(Qt.Horizontal, self)  # Horizontal slider
        sldr1.setMinimum(0)
        sldr1.setMaximum(100)
        sldr1.setValue(50)  # Set default volume
        layout.addWidget(sldr1, alignment=Qt.AlignCenter)

        # Radio buttons label
        optionlbl = QLabel("<b>Difficulty:</b>", self)
        optionlbl.setStyleSheet("color: lightblue")
        
        optionlbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(optionlbl)

        # Radio buttons
        radio_layout = QVBoxLayout()  # Add a nested layout for radio buttons
        radio_layout.setSpacing(5)  # Reduce spacing between radio buttons
        Easy = QRadioButton("Easy", self)
        Easy.setStyleSheet("color: green; font-size: 12px;")
        Easy.setCursor(Qt.PointingHandCursor)
        radio_layout.addWidget(Easy, alignment=Qt.AlignCenter)

        Medium = QRadioButton("Medium", self)
        Medium.setStyleSheet("color: blue; font-size: 12px;")
        Medium.setCursor(Qt.PointingHandCursor)
        radio_layout.addWidget(Medium, alignment=Qt.AlignCenter)

        Hard = QRadioButton("Hard", self)
        Hard.setStyleSheet("color: red; font-size: 12px;")
        Hard.setCursor(Qt.PointingHandCursor)
        radio_layout.addWidget(Hard, alignment=Qt.AlignCenter)

        layout.addLayout(radio_layout)

        # Close button
        self.close_button = QPushButton("Back to Main Menu", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)
        self.close_button.setStyleSheet("background-color: lightblue")
        self.close_button.setCursor(Qt.PointingHandCursor)

        # Set the layout for the settings window
        self.setLayout(layout)

    def center(self):   # Center the window on the screen
        
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)





class InstructionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Instructions")
        self.setGeometry(500, 400, 600, 600)  # Match other pages' sizes
        self.setStyleSheet("background-color: black")
        self.center()

        # Main layout for the page
        main_layout = QVBoxLayout(self)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: black;")
        
        # Scroll Area Content Widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Instructions title
        title = QLabel("Game Instructions", self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: lightblue")
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Instructions text
        instructions_text = """
        # Main Concept and Game Flow

        1. **Game Setup**:
            - Each player has a grid (often 10x10) to place ships in different orientations (horizontal or vertical).
            - Ships vary in size and can’t overlap. Common ships include:
                - **Carrier**: 5 squares
                - **Battleship**: 4 squares
                - **Cruiser**: 3 squares
                - **Submarine**: 3 squares
                - **Destroyer**: 2 squares
        2. **Objective**:
            - The goal is to locate and "sink" all of the opponent's ships before they sink yours.
        3. **Taking Turns**:
            - Players take turns guessing where the opponent's ships might be by choosing coordinates on their opponent’s grid.
            - After each guess, the result is revealed:
                - **Hit**: The guess landed on part of a ship.
                - **Miss**: The guess hit an empty part of the grid (ocean).
        4. **Rocket Mechanics (Firing Mechanism)**:
            - When a player "fires a rocket" (selects a coordinate), they’re hoping to hit a ship.
            - If a part of the ship is hit, the game visually marks it, often with an explosion animation or icon on that coordinate.
            - If it’s a miss, a water splash or "miss" marker shows up instead.
        5. **Tracking and Strategy**:
            - Players keep track of hits and misses to narrow down possible locations of the remaining ships.
            - When a ship is hit, players often focus on nearby coordinates to try and finish "sinking" it, as ships occupy multiple connected squares.
        6. **Winning the Game**:
            - A player wins by hitting all squares occupied by their opponent’s ships. Once all ships are fully "sunk," the game ends.

        **Ideas**: Land ships at an angle.
        """
        instructions_label = QLabel(instructions_text, self)
        instructions_label.setStyleSheet("color: white;")
        instructions_label.setWordWrap(True)
        content_layout.addWidget(instructions_label)

        # Add Back button
        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.close)
        back_button.setStyleSheet("background-color: lightblue; border-radius: 9px")
        content_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # Set the layout for the content widget
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)



# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    username_page = UsernamePage()
    username_page.show()
    sys.exit(app.exec_())
