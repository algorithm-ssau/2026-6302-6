import sys
import os
import json  # <-- ДОБАВИЛИ
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QFileDialog, QDialog, 
    QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt

from config import INITIAL_TEST_FILE, WINDOW_WIDTH, WINDOW_HEIGHT
from core.data_manager import DataManager
from ui.pages import MenuPage, QuizPage, ResultsPage, SummaryPage, HistoryPage, SelectionPage, LinksPage

# Импорт твоих модулей
from questions.Question import Question
from giga_module.giga_parser import parse_questions, parse_summary_tags
from giga_module.giga import GigaResponse


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GigaAnalyzer & Quiz v2.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.current_data = {"questions": [], "summary": ""}
        self.init_ui()

    def init_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем страницы
        self.menu_page = MenuPage(self)
        self.quiz_page = QuizPage(self)
        self.results_page = ResultsPage(self)
        self.summary_page = SummaryPage(self)
        self.history_page = HistoryPage(self)
        self.selection_page = SelectionPage(self)

        # Добавляем в стек (индексы должны совпадать с вызовами)
        self.central_widget.addWidget(self.menu_page)      # 0
        self.central_widget.addWidget(self.quiz_page)      # 1
        self.central_widget.addWidget(self.summary_page)   # 2
        self.central_widget.addWidget(self.selection_page) # 3
        self.central_widget.addWidget(self.history_page)   # 4

        self.central_widget.addWidget(self.results_page)   # 7

    def show_menu(self):
        self.central_widget.setCurrentIndex(0)

    def show_summary(self):
        self.summary_page.set_summary(self.current_data.get("summary", ""))
        self.central_widget.setCurrentIndex(2)

    def show_history(self):
        history = DataManager.load_history()
        self.history_page.update_list(history.keys())
        self.central_widget.setCurrentIndex(4)

    def show_links(self):
        self.central_widget.setCurrentIndex(6)

    def start_test(self, back_index=3):
        questions = self.current_data.get("questions", [])
        if not questions:
            print("Ошибка: нет вопросов для теста")
            return
        self.quiz_page.start_test(questions, back_index)
        self.central_widget.setCurrentIndex(1)

    def show_results(self, questions, user_answers):
        """Исправлено: передаем данные напрямую"""
        self.results_page.display_results(questions, user_answers)
        self.central_widget.setCurrentIndex(7)

    def start_assistant(self):
        self.assistant_page.render_node("start")
        self.central_widget.setCurrentIndex(5)

    def upload_user_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if not file_path:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Обработка")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Гигачат анализирует документ..."))
        dialog.show()
        QApplication.processEvents()

        try:
            raw = GigaResponse(file_path)
            questions = parse_questions(raw[0])
            summary_md = parse_summary_tags(raw[1])

            filename = os.path.basename(file_path)
            DataManager.save_to_history(filename, summary_md, questions)

            self.current_data = {
                "questions": questions,
                "summary": summary_md
            }
            self.summary_page.set_summary(summary_md)

            dialog.close()
            self.central_widget.setCurrentIndex(3)

        except Exception as e:
            dialog.close()
            print(f"Ошибка при обработке файла: {e}")

    def load_from_history(self, filename):
        data = DataManager.load_from_history(filename)
        if not data:
            return

        questions = [Question.from_dict(q) for q in data["questions"]]
        self.current_data = {
            "summary": data["summary"],
            "questions": questions
        }
        self.summary_page.set_summary(data["summary"])
        self.central_widget.setCurrentIndex(3)

    def start_initial_test(self):
        if not os.path.exists(INITIAL_TEST_FILE):
            print("Ошибка: Файл initial_test.json не найден")
            return

        try:
            with open(INITIAL_TEST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            questions = [Question.from_dict(q) for q in data]
            self.current_data = {
                "questions": questions,
                "summary": "Вступительный тест из локальной базы"
            }
            self.start_test(back_index=0)

        except Exception as e:
            print(f"Ошибка при загрузке начального теста: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
