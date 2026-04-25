from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QScrollArea, QFrame, QApplication
)
from PySide6.QtCore import Qt
from decision_tree.tree_data import DecisionNode, TREE_NODES


class DecisionTreeWidget(QWidget):
    def __init__(self, on_close_callback):
        super().__init__()
        self.on_close = on_close_callback
        self.history = []  # Для кнопки "Назад"
        self.current_node_id = "start"
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Заголовок
        self.title_label = QLabel("Помощник: Запрос информации")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(self.title_label)

        # Основной текст / Контент
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        self.content_area.setStyleSheet("background: #f9f9f9; border: 1px solid #ddd; padding: 10px; font-size: 14px;")
        self.layout.addWidget(self.content_area)

        # Кнопка копирования (появляется только в шаблонах)
        self.copy_btn = QPushButton("📋 Копировать образец")
        self.copy_btn.setVisible(False)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_btn)

        # Контейнер для кнопок выбора
        self.options_layout = QVBoxLayout()
        self.layout.addLayout(self.options_layout)

        # Нижняя панель управления
        self.nav_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Назад")
        self.back_btn.clicked.connect(self.go_back)
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(self.on_close)

        self.nav_layout.addWidget(self.back_btn)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.close_btn)
        self.layout.addLayout(self.nav_layout)

        self.render_node("start")

    def render_node(self, node_id):
        node = TREE_NODES[node_id]
        self.current_node_id = node_id

        # Обновляем текст
        display_text = node.text
        if node.content_type in ["address_list", "template"] and node.extra_data:
            display_text += f"\n\n{node.extra_data}"
        self.content_area.setText(display_text)

        # Настройка спец-элементов
        self.copy_btn.setVisible(node.content_type == "template")
        self.back_btn.setEnabled(len(self.history) > 0)
        self.close_btn.setVisible(node.show_close_button)

        # Очистка старых кнопок выбора
        for i in reversed(range(self.options_layout.count())):
            self.options_layout.itemAt(i).widget().setParent(None)

        # Создание новых кнопок
        for opt_text, next_id in node.options.items():
            btn = QPushButton(opt_text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked=False, nid=next_id: self.go_forward(nid))
            self.options_layout.addWidget(btn)

    def go_forward(self, next_id):
        self.history.append(self.current_node_id)
        self.render_node(next_id)

    def go_back(self):
        if self.history:
            prev_id = self.history.pop()
            self.render_node(prev_id)

    def copy_to_clipboard(self):
        node = TREE_NODES[self.current_node_id]
        if node.extra_data:
            QApplication.clipboard().setText(node.extra_data)