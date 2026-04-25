from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget

class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Выберите ранее загруженный файл:")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("font-size: 16px; padding: 10px;")

        btn_select = QPushButton("Открыть")
        btn_select.clicked.connect(self.load_selected)

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(self.go_back)

        layout.addWidget(label)
        layout.addWidget(self.history_list)
        layout.addWidget(btn_select)
        layout.addWidget(btn_back)

    def update_list(self, history_keys):
        self.history_list.clear()
        self.history_list.addItems(history_keys)

    def load_selected(self):
        item = self.history_list.currentItem()
        if item and self.parent_window:
            self.parent_window.load_from_history(item.text())

    def go_back(self):
        if self.parent_window:
            self.parent_window.show_menu()
