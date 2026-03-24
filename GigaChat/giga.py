from decouple import config
from gigachat import GigaChat

SECRET_KEY = config("GIGA_CREDENTIALS")
import json


def GigaResponse(filename:str) -> list[str]:
    with open('prompt.json', 'r', encoding='utf-8') as f:
        config_json = json.load(f)
        prompt_questions_template = config_json["Strict_Test_Generator_No_Formatting"]
    
    