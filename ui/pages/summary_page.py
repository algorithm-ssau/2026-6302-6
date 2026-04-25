from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

class SummaryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        btn_back = QPushButton("← Вернуться")
        btn_back.setFixedSize(150, 40)
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)

        self.summary_display = QTextEdit()
        self.summary_display.setReadOnly(True)
        self.summary_display.setStyleSheet(
            "font-size: 16px; padding: 15px; background: #f9f9f9; border: none;"
        )
        layout.addWidget(self.summary_display)

    def set_summary(self, text):
        self.summary_display.setMarkdown(text)

    def go_back(self):
        if self.parent_window:
            self.parent_window.central_widget.setCurrentIndex(3)
