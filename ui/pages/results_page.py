from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame
)
from PySide6.QtCore import Qt

class ResultsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Заголовок
        title = QLabel("Результаты тестирования")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        # Скролл область для результатов
        self.scroll = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)

        # Кнопка назад
        btn_back = QPushButton("Вернуться в меню")
        btn_back.setFixedSize(200, 50)
        btn_back.clicked.connect(self.go_back)
        self.layout.addWidget(btn_back, alignment=Qt.AlignCenter)

    def display_results(self, questions, user_answers):
        """
        Главный фикс: теперь принимаем questions и answers как параметры,
        а не пытаемся достать из self.parent_window
        """
        # Очищаем старые результаты
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not questions or not user_answers:
            error_label = QLabel("Ошибка: нет данных для отображения")
            error_label.setStyleSheet("color: red; font-size: 16px;")
            self.scroll_layout.addWidget(error_label)
            return

        correct_count = 0

        for i, q in enumerate(questions):
            if i >= len(user_answers):
                break

            u_ans = user_answers[i]
            # Правильный ответ всегда на 0 индексе в answers
            correct_ans_text = q.answers[0] if q.answers else "Нет ответа"
            is_correct = (u_ans == correct_ans_text)

            if is_correct:
                correct_count += 1

            color = "#2ecc71" if is_correct else "#e74c3c"  # Зеленый или Красный
            status = "✅ Верно" if is_correct else "❌ Неверно"

            # Карточка вопроса
            q_box = QFrame()
            q_box.setStyleSheet(f"""
                QFrame {{
                    border: 2px solid {color};
                    border-radius: 8px;
                    margin-bottom: 10px;
                    padding: 15px;
                    background: white;
                }}
            """)
            box_layout = QVBoxLayout(q_box)

            res_text = (
                f"<b style='color: #666;'>Тема: {q.theme}</b><br><br>"
                f"<span style='font-size: 16px;'><b>Вопрос:</b> {q.question}</span><br><br>"
                f"<b>Правильный ответ:</b> <span style='color: #2ecc71;'>{correct_ans_text}</span><br>"
                f"<b>Ваш ответ:</b> <span style='color: {color}; font-weight: bold;'>{u_ans}</span><br><br>"
                f"<b style='font-size: 18px;'>Статус: {status}</b>"
            )

            lbl = QLabel(res_text)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 14px; line-height: 1.4;")
            box_layout.addWidget(lbl)

            self.scroll_layout.addWidget(q_box)

        # Добавляем итоговый счет
        total = len(questions)
        score_label = QLabel(f"<h2>Итого: {correct_count} из {total} ({round(correct_count/total*100)}%)</h2>")
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setStyleSheet("margin: 20px 0; padding: 15px; background: #f0f0f0; border-radius: 8px;")
        self.scroll_layout.insertWidget(0, score_label)

        # Добавляем растяжку в конец
        self.scroll_layout.addStretch()

    def go_back(self):
        if self.parent_window:
            self.parent_window.show_menu()
