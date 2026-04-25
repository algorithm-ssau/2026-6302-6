class Question:
    def __init__(self, question: str, answers: list[str], theme: str) -> None:
        self.question = question
        self.answers = answers.copy()
        self.theme = theme
        self.correct_answer: int = 0

    def to_dict(self):
        return {
            "question": self.question,
            "answers": self.answers,
            "theme": self.theme
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["answers"], data["theme"])
        
    def __str__(self):
        return f"тема: {self.theme}, вопрос: {self.question}, правильный ответ: {self.answers[self.correct_answer]}"