import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import time


class TypingSpeedTestApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Typing Speed Test")
        self.setGeometry(100, 100, 500, 300)

        # Create widgets
        self.instructions = QLabel("Type the following text as quickly as you can:")
        self.sample_text = QLabel("The quick brown fox jumps over the lazy dog")
        self.typing_area = QLineEdit(self)
        self.result_label = QLabel("")
        self.start_button = QPushButton("Start", self)

        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.instructions)
        self.layout.addWidget(self.sample_text)
        self.layout.addWidget(self.typing_area)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.result_label)

        # Set the layout
        self.setLayout(self.layout)

        # Connect the button to start the test
        self.start_button.clicked.connect(self.start_test)

        # Variables for timing
        self.start_time = None

    def start_test(self):
        # Reset and start test
        self.start_button.setEnabled(False)  # Disable start button during test
        self.typing_area.setText('')  # Clear any previous text
        self.typing_area.setFocus()  # Focus on the typing area
        self.result_label.setText("")  # Clear any previous result

        # Start timing the test
        self.start_time = time.time()

        # Connect the typing area to check input as user types
        self.typing_area.textChanged.connect(self.track_input)

    def track_input(self):
        typed_text = self.typing_area.text()
        if typed_text == self.sample_text.text():
            # When the typing matches the sample, stop and show result
            time_taken = time.time() - self.start_time
            wpm = len(typed_text.split()) / (time_taken / 60)  # Words per minute calculation
            self.result_label.setText(f"Typing speed: {wpm:.2f} WPM")
            self.start_button.setEnabled(True)  # Re-enable the start button


# Initialize the application and the window
app = QApplication(sys.argv)
window = TypingSpeedTestApp()
window.show()

# Run the event loop
sys.exit(app.exec_())