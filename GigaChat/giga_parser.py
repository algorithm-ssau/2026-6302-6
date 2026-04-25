from typing import List
from questions.Question import Question
import re

def parse_gigachat_response(raw_text: str) -> List[Question]:
    # Очищаем от возможных случайных пробелов в начале/конце и разбиваем по строкам
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    
    questions_list = []
    
    # Шаг итерации — 6 строк (1 вопрос + 4 варианта + 1 тема)
    for i in range(0, len(lines), 6):
        # Проверяем, что у нас достаточно строк для формирования полного блока
        if i + 5 < len(lines):
            question_text = lines[i]
            # Ответы идут со 2-й по 5-ю строку блока
            answer_variants = lines[i+1 : i+5]
            theme_text = lines[i+5]
            
            # Создаем объект
            q_obj = Question(
                question=question_text,
                answers=answer_variants,
                theme=theme_text
            )
            questions_list.append(q_obj)
            
    return questions_list

def parse_questions(raw_text: str) -> List[Question]:
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    questions_list = []
    for i in range(0, len(lines), 6):
        if i + 5 < len(lines):
            questions_list.append(Question(lines[i], lines[i+1 : i+5], lines[i+5]))
    return questions_list

def parse_summary_tags(raw_text: str) -> str:
    # Ищем контент между [SUMMARY_START] и [SUMMARY_END] и другими тегами
    # Но для вывода в приложении объединим их в красивый Markdown
    def get_tag(tag, text):
        match = re.search(rf"\[{tag}_START\](.*?)\[{tag}_END\]", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    title = get_tag("TITLE", raw_text)
    summary = get_tag("SUMMARY", raw_text)
    points = get_tag("POINTS", raw_text)

    # Формируем итоговый Markdown текст
    formatted_text = f"# {title}\n\n"
    formatted_text += f"## Краткое содержание\n{summary}\n\n"
    formatted_text += f"## Ключевые тезисы\n{points}"
    return formatted_text