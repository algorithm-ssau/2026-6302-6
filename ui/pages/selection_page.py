from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class SelectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Файл обработан. Что вы хотите сделать?")
        label.setStyleSheet("font-size: 20px; margin-bottom: 20px;")

        btn_sum = QPushButton("Посмотреть краткое содержание")
        btn_sum.setFixedSize(350, 60)
        btn_sum.clicked.connect(self.show_summary)

        btn_test = QPushButton("Пройти тест по материалу")
        btn_test.setFixedSize(350, 60)
        btn_test.clicked.connect(self.start_test)

        btn_back = QPushButton("← Назад в меню")
        btn_back.clicked.connect(self.go_back)

        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(btn_sum, alignment=Qt.AlignCenter)
        layout.addWidget(btn_test, alignment=Qt.AlignCenter)
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)

    def show_summary(self):
        if self.parent_window:
            self.parent_window.show_summary()

    def start_test(self):
        if self.parent_window:
            self.parent_window.start_test()

    def go_back(self):
        if self.parent_window:
            self.parent_window.show_menu()
