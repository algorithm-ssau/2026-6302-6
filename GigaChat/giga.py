from decouple import config
from gigachat import GigaChat

SECRET_KEY = config("GIGA_CREDENTIALS")
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def GigaResponse(filename:str) -> list[str]:
    with open(resource_path('prompt.json'), 'r', encoding='utf-8') as f:
        config_json = json.load(f)
        prompt_questions_template = config_json["Strict_Test_Generator_No_Formatting"]
        prompt_summary_template = config_json["Document_Analyzer_Strict_Tags"]
    
    with GigaChat(credentials=SECRET_KEY,verify_ssl_certs=False,scope="GIGACHAT_API_PERS",model="GigaChat-2",timeout=360) as client:
        with open(filename, "rb") as f:
            uploaded = client.upload_file(f, purpose="general")
        print(f"Файл загружен: {uploaded.id_}")
        


        result = client.chat(
        {
            # "function_call": "auto",
            "messages": [
                {
                    "role": "system",
                    "content": prompt_questions_template,
                    
                },
                {
                    "role": "user",
                    "content": "Выдай ответ согласно заданным условиям",
                    "attachments": [uploaded.id_],
                }
            ],
            "temperature": 0.1
        }
        )
        # print(result.choices[0].message.content)

        answer = []
        answer.append(result.choices[0].message.content)
        result = client.chat(
        {
            # "function_call": "auto",
            "messages": [
                {
                    "role": "system",
                    "content": prompt_summary_template,
                    
                },
                {
                    "role": "user",
                    "content": "Выдай ответ согласно заданным условиям",
                    "attachments": [uploaded.id_],
                }
            ],
            "temperature": 0.1
        }
        )
        # print(result.usage)
        answer.append(result.choices[0].message.content)
        return answer