from decouple import config
from gigachat import GigaChat

SECRET_KEY = config("GIGA_CREDENTIALS")
import json


def GigaResponse(filename:str) -> list[str]:
    with open('prompt.json', 'r', encoding='utf-8') as f:
        config_json = json.load(f)
        prompt_questions_template = config_json["Strict_Test_Generator_No_Formatting"]
    
    with GigaChat(credentials=SECRET_KEY,verify_ssl_certs=False) as client:
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
        print(result.choices[0].message.content)

        answer = []
        answer.append(result.choices[0].message.content)
        return answer