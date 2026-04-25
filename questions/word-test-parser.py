import docx2txt
import json
from Question import Question

file = docx2txt.process("../files_with_tests/Билет-№-1.docx")
text = file.splitlines()
text.pop(0)
text.pop(0)


questions: list[Question] = list()


i = 0
while i < len(text):
    line = text[i]
    clean_line = " ".join(line.split())
    if clean_line == '\n' or clean_line == '':
        i += 1
        continue

    if clean_line[0].isdigit():
        answers = list()
        question = None
        j = i
        while True:
            if j >= len(text):
                i = j
                break
            line_j = text[j]
            clean_line_j = " ".join(line_j.split())
            if clean_line_j == '\n' or clean_line_j == '':
                j += 1
                continue

            if clean_line_j[0].isdigit() and question is not None:
                questions.append(Question(question, answers, "empty theme"))
                i = j
                break

            if clean_line_j[0].isdigit():
                question = clean_line_j.split('.')[1].strip()
                j += 1
                continue
            else:
                answers.append(clean_line_j.split(')')[1].strip())

            j += 1

file_otveti = docx2txt.process("../files_with_tests/ОТВЕТЫ.docx")
text_otveti = file_otveti.split("Билет")[1].split("Ответ")


otveti = list()
for otvet in text_otveti[1]:
    if otvet != ' ' and otvet != '\n':
        otveti.append(otvet)

print(otveti)

start_code = ord('А')

indices = [ord(char) - start_code for char in otveti]

for i in range(0, len(indices)):
    if i < len(questions):
        # Обращаемся к списку ответов конкретного вопроса
        answers_list = questions[i].answers
        idx = indices[i]
        # Меняем местами, чтобы правильный ответ всегда был под индексом 0
        # (или согласно вашей логике)
        if idx < len(answers_list):
            answers_list[0], answers_list[idx] = answers_list[idx], answers_list[0]


with open("../initial_test.json", "w", encoding="utf-8") as f:
    json.dump([q.to_dict() for q in questions], f, ensure_ascii=False, indent=2)

print(f"Готово! Сохранено {len(questions)} вопросов в initial_test.json")

