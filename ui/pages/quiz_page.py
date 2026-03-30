from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt
import random

class QuizPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.current_q_index = 0
        self.user_answers = []
        self.questions = []
        self.back_index = 0
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Кнопка назад
        btn_back = QPushButton("← Прекратить тест")
        btn_back.clicked.connect(self.stop_quiz)
        self.layout.addWidget(btn_back, alignment=Qt.AlignLeft)

        # Тема
        self.topic_label = QLabel("Тема: ")
        self.topic_label.setStyleSheet("color: gray; font-size: 14px; margin-top: 10px;")
        self.layout.addWidget(self.topic_label)

        # Вопрос
        self.q_label = QLabel("Текст вопроса")
        self.q_label.setWordWrap(True)
        self.q_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px 0px;")
        self.layout.addWidget(self.q_label)

        # Контейнер для вариантов
        self.options_container = QVBoxLayout()
        self.btn_group = QButtonGroup(self)
        self.layout.addLayout(self.options_container)

        self.layout.addStretch()

        # Кнопка далее
        self.next_btn = QPushButton("Далее")
        self.next_btn.setFixedSize(120, 40)
        self.next_btn.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_btn, alignment=Qt.AlignRight)

    def start_test(self, questions, back_index=0):
        """Запуск теста с заданными вопросами"""
        self.questions = questions
        self.back_index = back_index
        self.current_q_index = 0
        self.user_answers = []
        self.load_question()

    def load_question(self):
        # Очищаем старые варианты
        while self.options_container.count():
            item = self.options_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.btn_group = QButtonGroup(self)

        if self.current_q_index >= len(self.questions):
            return

        q_obj = self.questions[self.current_q_index]
        shuffled = q_obj.answers.copy()
        random.shuffle(shuffled)

        self.topic_label.setText(f"Тема: {q_obj.theme}")
        self.q_label.setText(f"Вопрос {self.current_q_index + 1} из {len(self.questions)}:\n{q_obj.question}")

        for opt in shuffled:
            btn = QRadioButton(opt)
            btn.setStyleSheet("font-size: 16px; padding: 5px;")
            self.options_container.addWidget(btn)
            self.btn_group.addButton(btn)

        # Меняем текст кнопки для последнего вопроса
        if self.current_q_index == len(self.questions) - 1:
            self.next_btn.setText("Завершить")
        else:
            self.next_btn.setText("Далее")

    def next_question(self):
        btn = self.btn_group.checkedButton()
        self.user_answers.append(btn.text() if btn else "Нет ответа")

        if self.current_q_index < len(self.questions) - 1:
            self.current_q_index += 1
            self.load_question()
        else:
            self.finish_test()

    def finish_test(self):
        if self.parent_window:
            self.parent_window.show_results(self.questions, self.user_answers)

    def stop_quiz(self):
        if self.parent_window:
            self.parent_window.central_widget.setCurrentIndex(self.back_index)
