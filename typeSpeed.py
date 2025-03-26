import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, \
    QFormLayout, QColorDialog
from PyQt5.QtCore import QTimer

# Predefined list of sample sentences
sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a great programming language for automation.",
    "PyQt5 is a set of Python bindings for Qt libraries.",
    "Typing speed is measured in words per minute.",
    "This is a random sentence for typing speed testing."
]


class TypingSpeedApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the main window with default values
        self.font_size = 12  # Default font size
        self.bg_color = "#ffffff"  # Default background color
        self.text_color = "#000000"  # Default text color

        self.initUI()

        self.start_time = None
        self.timer = None

    def initUI(self):
        """Initialize the GUI components"""
        self.setWindowTitle('Typing Speed Tracker')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Start Test and Settings buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton('Start Test', self)
        self.start_button.clicked.connect(self.start_test)
        button_layout.addWidget(self.start_button)

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        button_layout.addWidget(self.settings_button)

        layout.addLayout(button_layout)

        # Display text to type
        self.text_to_type_label = QLabel("Press 'Start Test' to begin", self)
        self.text_to_type_label.setStyleSheet(f"font-size: {self.font_size}px; color: {self.text_color};")
        layout.addWidget(self.text_to_type_label)

        # User input box
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Start typing here...")
        self.user_input.setReadOnly(True)  # Initially not editable until test starts
        self.user_input.setStyleSheet(f"font-size: {self.font_size}px; color: {self.text_color};")
        layout.addWidget(self.user_input)

        # Typing speed label
        self.typing_speed_label = QLabel("Typing Speed: 0 WPM", self)
        self.typing_speed_label.setStyleSheet(f"font-size: {self.font_size}px; color: {self.text_color};")
        layout.addWidget(self.typing_speed_label)

        # Set the layout for the main window
        self.setLayout(layout)

    def start_test(self):
        """Start the typing test when the user clicks Start Test"""
        # Select a random sentence from the sample list
        self.selected_text = random.choice(sample_texts)

        # Set the random sentence as the text to type
        self.text_to_type_label.setText(f"Type this: {self.selected_text}")

        # Clear the user input box and enable it for typing
        self.user_input.clear()
        self.user_input.setReadOnly(False)
        self.user_input.setFocus()

        # Start the timer
        self.start_time = time.time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_typing_speed)
        self.timer.start(1000)  # Update typing speed every second

    def update_typing_speed(self):
        """Update typing speed every second while typing"""
        if self.start_time:
            # Get the elapsed time in minutes
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 0:
                typed_text = self.user_input.text()

                # Calculate the word count (a word is considered to be a group of characters separated by spaces)
                word_count = len(typed_text.split())

                # Calculate words per minute (WPM)
                wpm = word_count / (elapsed_time / 60)

                # Update the typing speed label
                self.typing_speed_label.setText(f"Typing Speed: {int(wpm)} WPM")

                # Check if the user has typed the entire sentence correctly
                if typed_text == self.selected_text:
                    self.timer.stop()
                    self.typing_speed_label.setText(f"Typing Speed: {int(wpm)} WPM - Test Complete!")
                    self.user_input.setReadOnly(True)  # Disable further typing after completion

    def open_settings(self):
        """Open settings window"""
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def apply_settings(self, font_size, bg_color, text_color, new_sentences):
        """Apply the settings changes to the main window"""
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color

        # Apply font size and colors to UI components
        self.text_to_type_label.setStyleSheet(f"font-size: {self.font_size}px; color: {self.text_color};")
        self.user_input.setStyleSheet(f"font-size: {self.font_size}px; color: {self.text_color};")
        self.typing_speed_label.setStyleSheet(f"font-size: {self.font_size}px; color: {self.text_color};")
        self.setStyleSheet(f"background-color: {self.bg_color};")

        # Add new sentences to the sample_texts list
        global sample_texts
        sample_texts = new_sentences


class SettingsWindow(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        # Font size input
        self.font_size_input = QLineEdit(self)
        self.font_size_input.setText(str(parent.font_size))  # Load current font size
        self.layout.addRow("Font Size:", self.font_size_input)

        # Background color input
        self.bg_color_button = QPushButton('Choose Background Color', self)
        self.bg_color_button.clicked.connect(self.change_bg_color)
        self.layout.addRow(self.bg_color_button)

        # Text color input
        self.text_color_button = QPushButton('Choose Text Color', self)
        self.text_color_button.clicked.connect(self.change_text_color)
        self.layout.addRow(self.text_color_button)

        # Add new sentence input
        self.new_sentence_input = QLineEdit(self)
        self.layout.addRow("Add Sentence:", self.new_sentence_input)

        # Save button to store settings
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addRow(self.save_button)

        self.setLayout(self.layout)

        # Store references to parent class
        self.parent = parent

    def save_settings(self):
        """Save the updated settings and close the settings window"""
        # Get values from input fields
        font_size = int(self.font_size_input.text())
        bg_color = self.parent.bg_color  # Current bg color
        text_color = self.parent.text_color  # Current text color

        # Add the new sentence to the sample sentences
        new_sentence = self.new_sentence_input.text()
        if new_sentence:
            sample_texts.append(new_sentence)

        # Apply changes to the main window
        self.parent.apply_settings(font_size, bg_color, text_color, sample_texts)

        # Close the settings window
        self.close()

    def change_bg_color(self):
        """Open color dialog for background color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent.bg_color = color.name()

    def change_text_color(self):
        """Open color dialog for text color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent.text_color = color.name()


def main():
    app = QApplication(sys.argv)
    window = TypingSpeedApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()