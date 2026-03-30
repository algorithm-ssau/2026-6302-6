import json
import os
from config import HISTORY_FILE

class DataManager:
    @staticmethod
    def load_history():
        if not os.path.exists(HISTORY_FILE):
            return {}
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_to_history(filename, summary, questions):
        history = DataManager.load_history()

        # Преобразуем объекты Question в словари
        questions_dict = [q.to_dict() for q in questions]

        history[filename] = {
            "summary": summary,
            "questions": questions_dict
        }

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_from_history(filename):
        history = DataManager.load_history()
        if filename not in history:
            return None
        return history[filename]
