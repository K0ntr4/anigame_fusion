import io
import os
import sys
import threading
import time

from PySide6.QtWidgets import (  # pylint: disable=E0611
    QApplication, QMainWindow, QLabel,
    QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QImage  # pylint: disable=E0611
from PySide6.QtCore import Qt  # pylint: disable=E0611
from src.image.game_info import GameInfo
from src.image.text_to_image import create_image
from src.image.character_info import get_closest_characters


def read_stylesheet(file_path):
    """
    Read the contents of a stylesheet file.

    Args:
        file_path (str): The path to the stylesheet file.

    Returns:
        str: The contents of the stylesheet file.
    """
    if not os.path.exists(file_path):
        return None
    with open(file=file_path, encoding='utf-8', mode='r') as file:
        return file.read()


def pil2pixmap(image):
    """
    Convert a PIL image to a QPixmap.

    Args:
        image (PIL.Image): The input PIL image to convert.

    Returns:
        QPixmap: The converted QPixmap.
    """
    bytes_img = io.BytesIO()
    image.save(bytes_img, format='PNG')
    qimg = QImage()
    qimg.loadFromData(bytes_img.getvalue())
    return QPixmap.fromImage(qimg)


class AnimeImageGenerator:
    """
    Class responsible for generating anime images.
    """

    def __init__(self):
        """
        Initialize AnimeImageGenerator.
        """
        self.last_input_values = {}
        self.output_filename = None
        self.images = []
        self.current_index = 0

    def process_image(self, input_values, window_element):
        """
        Process an image based on input values.

        Args:
            input_values (dict): A dictionary containing input values.
            window_element: The window element to update with the generated image.
        """
        window_element.input_controls["progress_label"].setText("Generating image...")
        game_info = GameInfo()
        recency, game_tags = game_info.get_game_keywords(input_values["game_name"])
        input_values["processed_anime_name"] = (
            get_closest_characters(input_values["anime_name"]))
        input_values.update({"recency": recency, "game_tags": game_tags})

        if input_values == self.last_input_values and self.output_filename:
            window_element.image_controls["image_label"].show()
            window_element.show_image()
        else:
            self.images, self.output_filename = create_image(input_values)
            window_element.show_image()
            self.last_input_values = input_values

    def save_image(self):
        """
        Save the current image.
        """
        if self.output_filename:
            full_filename = f'{self.output_filename}-{time.strftime("%Y%m%d-%H%M%S")}.png'
            self.images[self.current_index].save(full_filename)
            print(f"Image saved as: {full_filename}")


class AnimeCharacterImageGenerator(QMainWindow):
    """
    Class representing the main window of the Anime Character Image Generator application.
    """

    def __init__(self):
        """
        Initialize AnimeCharacterImageGenerator.
        """
        super().__init__()
        self.image_generator = AnimeImageGenerator()
        self.inputs = {
            "anime_name": QLineEdit(),
            "game_name": QLineEdit(),
            "facial_expression": QLineEdit("smile"),
            "looking_at": QLineEdit("viewer"),
            "indoors": QLineEdit("indoors"),
            "daytime": QLineEdit("night"),
            "additional_tags": QLineEdit()
        }
        self.inputs_labels = {
            "anime_name": "Anime character name",
            "game_name": "Game name",
            "facial_expression": "Facial expression",
            "looking_at": "Looking at",
            "indoors": "Indoors/outdoors",
            "daytime": "Daytime/night",
            "additional_tags": "Additional tags (Separated by commas)"
        }
        self.input_controls = {
            "progress_label": QLabel(""),
            "generate_button": QPushButton("Generate Image")
        }
        self.inputs_layout = None
        self.image_controls = {
            "image_label": QLabel(""),
            "back_button": QPushButton("Back"),
            "save_button": QPushButton("Save Image")
        }
        self.image_navigation_buttons = {
            "prev_button": QPushButton("<"),
            "next_button": QPushButton(">"),
        }
        self.setup_ui()
        self.show_input_fields()

    def setup_ui(self):
        """
        Set up the user interface.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Inputs
        self.inputs_layout = QVBoxLayout()
        for key, input_widget in self.inputs.items():
            self.inputs_layout.addWidget(QLabel(self.inputs_labels[key]))
            self.inputs_layout.addWidget(input_widget)
        layout.addLayout(self.inputs_layout)

        # Input controls
        self.input_controls["generate_button"].clicked.connect(self.generate_image)
        self.input_controls["progress_label"].setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image controls
        self.image_controls["image_label"].setScaledContents(True)
        self.image_controls["back_button"].clicked.connect(self.show_input_fields)
        self.image_navigation_buttons["prev_button"].clicked.connect(self.show_previous_image)
        self.image_navigation_buttons["next_button"].clicked.connect(self.show_next_image)
        self.image_controls["save_button"].clicked.connect(self.image_generator.save_image)

        # Image navigation buttons
        navigation_button_layout = QHBoxLayout()
        navigation_button_layout.addWidget(self.image_navigation_buttons["prev_button"])
        navigation_button_layout.addWidget(self.image_navigation_buttons["next_button"])

        # Add all elements to the layout
        for item in self.image_controls.values():
            layout.addWidget(item)
        layout.addLayout(navigation_button_layout)
        for item in self.input_controls.values():
            layout.addWidget(item)
        central_widget.setLayout(layout)

    def generate_image(self):
        """
        Generate an image based on user input.
        """
        if not self.inputs["game_name"].text():
            self.input_controls["progress_label"].setText(
                "Please enter a game name.")
            return
        if not self.inputs["anime_name"].text():
            self.input_controls["progress_label"].setText(
                "Please enter an anime character name.")
            return
        self.input_controls["generate_button"].setDisabled(True)

        input_values = {key: widget.text().lower().replace(',', ' ').lstrip().rstrip()
                        for key, widget in self.inputs.items()}

        threading.Thread(target=self.image_generator.process_image,
                         args=(input_values, self)).start()

    def show_image(self):
        """
        Show the generated image.
        """
        self.setWindowTitle(self.image_generator.output_filename)

        for i in range(self.inputs_layout.count()):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                widget.hide()

        for item in self.input_controls.values():
            item.hide()

        for item in self.image_controls.values():
            item.show()

        if len(self.image_generator.images) != 1:
            for item in self.image_navigation_buttons.values():
                item.show()

        pixmap = pil2pixmap(self.image_generator.images[self.image_generator.current_index])
        self.image_controls["image_label"].setPixmap(pixmap)

    def show_input_fields(self):
        """
        Show the input fields.
        """
        self.setWindowTitle("Anime Character Image Generator")
        self.input_controls["progress_label"].clear()

        for item in self.image_controls.values():
            item.hide()
        for item in self.image_navigation_buttons.values():
            item.hide()

        for i in range(self.inputs_layout.count()):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                widget.show()

        for item in self.input_controls.values():
            item.show()
        self.input_controls["generate_button"].setEnabled(True)

    def show_previous_image(self):
        """
        Show the previous image.
        """
        if self.image_generator.current_index > 0:
            self.image_generator.current_index -= 1
            self.show_image()

    def show_next_image(self):
        """
        Show the next image.
        """
        if self.image_generator.current_index < len(self.image_generator.images) - 1:
            self.image_generator.current_index += 1
            self.show_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylesheet = read_stylesheet('./resources/form.css')
    if stylesheet:
        app.setStyleSheet(stylesheet)
    window = AnimeCharacterImageGenerator()
    window.resize(1000, 1000)
    window.show()
    sys.exit(app.exec())
