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

Если в проекте используется `requirements.txt`, можно установить так:

```bash
uv pip install -r requirements.txt
```

## Запуск проекта

Варианты запуска зависят от структуры проекта.

### Если есть точка входа `main.py`

```bash
uv run python main.py
```

### Если запуск через модуль (пример)

```bash
uv run python -m <module_name>
```

### Если нужен просто интерактивный запуск скрипта

```bash
uv run python <script.py>
```

## Актуальный релиз uv

Ссылка на последний релиз: https://github.com/astral-sh/uv/releases/latest
