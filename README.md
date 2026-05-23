# 2026-6302-6

## Требования

- Python 3.10+ (рекомендуется 3.11+)
- [uv](https://github.com/astral-sh/uv) — быстрый менеджер зависимостей и виртуальных окружений

## Установка uv

### Вариант 1: через официальный установщик (рекомендуется)

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Проверьте установку:

```bash
uv --version
```

### Вариант 2: через pipx

```bash
pipx install uv
```

## Установка зависимостей через uv

В корне репозитория:

```bash
uv sync
```

## Запуск проекта

### 1. Зарегистрироваться на https://developers.sber.ru/
### 2. Получить Authorization key
### 3. Переименовать файл .env_example в .env и вставить свой ключ

macOS / Linux:

```bash
mv .env_example .env
```

Windows (PowerShell):

```powershell
Rename-Item -Path ".env_example" -NewName ".env"
```

### 6. В `config.py` в переменную `MODEL` вписать необходимую модель
Доступные варианты
```commandline
GigaChat-2
GigaChat-2-Pro
GigaChat-2-Max
```

### 5. Запустить `main.py`

```bash
uv run main.py
```

## Скачать .exe файл 

Ссылка на последний релиз: https://github.com/algorithm-ssau/2026-6302-6/releases
