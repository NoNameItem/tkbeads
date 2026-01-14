# Срез 1: Skeleton — Дизайн

## Структура файлов

```
src/tkbeads/
├── __init__.py      # Пустой, делает пакет
├── __main__.py      # Entry point
├── app.py           # TkbeadsApp
└── styles/
    └── app.tcss     # Стили

tests/
├── __init__.py      # Пустой
└── test_app.py      # Тест запуска/выхода
```

## Изменения

| Действие | Файл |
|----------|------|
| Удалить | `main.py` |
| Создать | `src/tkbeads/__init__.py` |
| Создать | `src/tkbeads/__main__.py` |
| Создать | `src/tkbeads/app.py` |
| Создать | `src/tkbeads/styles/app.tcss` |
| Создать | `tests/__init__.py` |
| Создать | `tests/test_app.py` |

## Компоненты

### `__main__.py`

```python
from tkbeads.app import TkbeadsApp

def main():
    app = TkbeadsApp()
    app.run()

if __name__ == "__main__":
    main()
```

### `app.py`

- Класс `TkbeadsApp(App)`
- `TITLE = "tkbeads"`
- Binding: `q` → `quit`
- Загрузка `app.tcss`

### `app.tcss`

- Минимальные стили
- Тёмный фон для Screen

### `test_app.py`

```python
async def test_app_starts_and_quits():
    app = TkbeadsApp()
    async with app.run_test() as pilot:
        assert app.is_running
        await pilot.press("q")
    assert not app.is_running
```

## Критерий готовности

- `python -m tkbeads` запускает приложение
- Экран с заголовком "tkbeads"
- `q` закрывает приложение
- Тест проходит
