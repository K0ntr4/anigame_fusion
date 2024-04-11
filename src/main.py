import io
import sys
import threading
from PySide6.QtWidgets import (  # pylint: disable=E0611
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout)
from PySide6.QtGui import QPixmap, QImage  # pylint: disable=E0611
from src.image.game_info import GameInfo
from src.image.text_to_image import create_image


def pil2pixmap(image):
    bytes_img = io.BytesIO()
    image.save(bytes_img, format='PNG')
    qimg = QImage()
    qimg.loadFromData(bytes_img.getvalue())
    return QPixmap.fromImage(qimg)


class AnimeImageGenerator:
    def __init__(self):
        self.last_input_values = {}
        self.output_filename = None
        self.images = []
        self.current_index = 0

    def process_image(self, input_values, window_element):
        window_element.input_controls["progress_label"].setText("Generating image...")
        game_info = GameInfo()
        recency, game_tags = game_info.get_game_keywords(input_values["game_name"])
        input_values.update({"recency": recency, "game_tags": game_tags})

        if input_values == self.last_input_values and self.output_filename:
            window_element.image_controls["image_label"].show()
            window_element.show_image()
        else:
            self.images, self.output_filename = create_image(input_values)
            window_element.show_image()
            self.last_input_values = input_values

    def save_image(self):
        if self.output_filename:
            pixmap = pil2pixmap(self.images[self.current_index])
            pixmap.save(self.output_filename)
            print(f"Image saved as: {self.output_filename}")


class AnimeCharacterImageGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inputs_layout = None
        self.inputs = {
            "anime_name": QLineEdit(),
            "gender": QLineEdit("1boy"),
            "game_name": QLineEdit(),
            "facial_expression": QLineEdit("smile"),
            "looking_at": QLineEdit("viewer"),
            "indoors": QLineEdit("indoors"),
            "daytime": QLineEdit("night"),
            "additional_tags": QLineEdit()
        }
        self.input_controls = {
            "generate_button": QPushButton("Generate Image"),
            "progress_label": QLabel("")
        }
        self.image_controls = {
            "image_label": QLabel(""),
            "back_button": QPushButton("Back"),
            "save_button": QPushButton("Save Image")
        }
        self.image_navigation_buttons = {
            "prev_button": QPushButton("<"),
            "next_button": QPushButton(">"),
        }

        self.setWindowTitle("Anime Character Image Generator")
        self.image_generator = AnimeImageGenerator()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.inputs_layout = QVBoxLayout()

        for label_text, input_widget in self.inputs.items():
            self.inputs_layout.addWidget(QLabel(label_text))
            self.inputs_layout.addWidget(input_widget)
        layout.addLayout(self.inputs_layout)

        self.input_controls["generate_button"].clicked.connect(self.generate_image)

        self.image_controls["image_label"].setScaledContents(True)

        self.image_controls["back_button"].clicked.connect(self.show_input_fields)
        self.image_controls["back_button"].hide()

        self.image_navigation_buttons["prev_button"].clicked.connect(self.show_previous_image)
        self.image_navigation_buttons["prev_button"].hide()

        self.image_navigation_buttons["next_button"].clicked.connect(self.show_next_image)
        self.image_navigation_buttons["next_button"].hide()

        navigation_button_layout = QHBoxLayout()
        navigation_button_layout.addWidget(self.image_navigation_buttons["prev_button"])
        navigation_button_layout.addWidget(self.image_navigation_buttons["next_button"])
        layout.addLayout(navigation_button_layout)

        self.image_controls["save_button"].clicked.connect(self.image_generator.save_image)
        self.image_controls["save_button"].hide()

        for item in self.input_controls.values():
            layout.addWidget(item)
        for item in self.image_controls.values():
            layout.addWidget(item)
        central_widget.setLayout(layout)

    def generate_image(self):
        input_values = {key: widget.text().lower().replace(',', ' ')
                        for key, widget in self.inputs.items()}
        threading.Thread(target=self.image_generator.process_image,
                         args=(input_values, self)).start()

    def show_image(self):
        self.setWindowTitle(self.image_generator.output_filename)
        self.input_controls["progress_label"].clear()

        for i in range(self.inputs_layout.count()):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                widget.hide()

        for item in self.input_controls.values():
            item.hide()
        for item in self.image_controls.values():
            item.show()

        pixmap = pil2pixmap(self.image_generator.images[self.image_generator.current_index])
        self.image_controls["image_label"].setPixmap(pixmap)

        if len(self.image_generator.images) == 1:
            self.image_navigation_buttons["prev_button"].hide()
            self.image_navigation_buttons["next_button"].hide()
        else:
            self.image_navigation_buttons["prev_button"].show()
            self.image_navigation_buttons["next_button"].show()

    def show_input_fields(self):
        self.setWindowTitle("Anime Character Image Generator")
        self.image_controls["image_label"].clear()
        self.image_controls["image_label"].hide()
        self.input_controls["progress_label"].clear()
        self.input_controls["progress_label"].show()

        for i in range(self.inputs_layout.count()):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                widget.show()

        self.input_controls["generate_button"].show()
        for item in self.image_controls.values():
            item.hide()

    def show_previous_image(self):
        if self.image_generator.current_index > 0:
            self.image_generator.current_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.image_generator.current_index < len(self.image_generator.images) - 1:
            self.image_generator.current_index += 1
            self.show_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnimeCharacterImageGenerator()
    window.resize(1000, 1000)
    window.show()
    sys.exit(app.exec())
