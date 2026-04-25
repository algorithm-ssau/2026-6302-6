from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class MenuPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Giga Service")
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignCenter)

        buttons_data = [
            ("Загрузить новый файл", self.upload_file),
            ("Начальное тестирование", self.start_initial),
            ("Использовать загруженные файлы", self.show_history),
            ("Запрос информации (Помощник)", self.start_assistant),
            ("Полезные ссылки", self.show_links)
        ]

        layout.addWidget(title)

        for text, callback in buttons_data:
            btn = QPushButton(text)
            btn.setFixedSize(300, 60)
            btn.clicked.connect(callback)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

    def upload_file(self):
        if self.parent_window:
            self.parent_window.upload_user_file()

    def start_initial(self):
        if self.parent_window:
            self.parent_window.start_initial_test()

    def show_history(self):
        if self.parent_window:
            self.parent_window.show_history()

    def start_assistant(self):
        if self.parent_window:
            self.parent_window.start_assistant()

    def show_links(self):
        if self.parent_window:
            self.parent_window.show_links()
