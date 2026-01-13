# tkbeads — TUI для Beads Task Tracker

## Обзор

TUI-приложение на Python для работы с [Beads](https://github.com/steveyegge/beads) — распределённым трекером задач для AI-агентов.

**Ключевые решения:**
- Библиотека: Textual
- Интеграция: прямой доступ к `.beads/issues.jsonl`
- Автообновление: file watcher

## Архитектура

```
┌─────────────────────────────────────┐
│           UI Layer (Textual)        │
│  KanbanScreen → TaskDetailModal     │
├─────────────────────────────────────┤
│          State Layer                │
│  TaskStore (reactive state)         │
├─────────────────────────────────────┤
│          Data Layer                 │
│  BeadsLoader + FileWatcher          │
└─────────────────────────────────────┘
```

**Поток данных:**
```
FileWatcher → BeadsLoader → TaskStore → UI обновляется
```

При изменении статуса:
```
UI action → TaskStore.update_status() → BeadsLoader.save() → файл обновлён
```

## Модель данных

```python
@dataclass
class Task:
    id: str              # "bd-a1b2" или "bd-a1b2.1"
    title: str
    status: Status       # open | in_progress | blocked | closed
    priority: int        # 0 = highest
    description: str
    created_at: datetime
    updated_at: datetime
    blockers: list[str]  # ID задач, которые блокируют эту
    parent_id: str | None

class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    CLOSED = "closed"
```

## UI-компоненты

### Kanban Board

```
┌──────────────┬──────────────┬──────────────┬─────────────┐
│   BLOCKED    │    READY     │ IN PROGRESS  │   CLOSED    │
│     (1)      │     (3)      │     (2)      │    (47)     │
├──────────────┼──────────────┼──────────────┼─────────────┤
│  Deploy CI   │ ▶ Setup DB   │   Auth API   │  Init repo  │
│              │   Add tests  │   Frontend   │  Schema     │
│              │   Docs       │              │  ...        │
└──────────────┴──────────────┴──────────────┴─────────────┘
```

**Логика колонок:**
- BLOCKED: `status == open` И есть открытые блокеры
- READY: `status == open` И нет открытых блокеров
- IN PROGRESS: `status == in_progress`
- CLOSED: `status == closed`

### Горячие клавиши

**Kanban Screen:**

| Клавиша | Действие |
|---------|----------|
| ←/→ | Переключение между колонками |
| ↑/↓ | Выбор задачи в колонке |
| Enter | Открыть детали задачи |
| q | Выход |

**Task Detail Modal:**

| Клавиша | Действие |
|---------|----------|
| Esc | Закрыть |
| Tab | Переключение между кнопками статуса |
| Enter | Применить статус |

### Textual-виджеты

```python
class KanbanBoard(Horizontal):
    """Контейнер для 4 колонок"""

class KanbanColumn(Vertical):
    """Одна колонка: заголовок + список задач"""

class TaskCard(Static):
    """Карточка задачи: id, title, priority"""

class TaskDetailModal(ModalScreen):
    """Модальное окно с деталями и сменой статуса"""
```

## Структура проекта

```
tkbeads/
├── pyproject.toml
├── src/
│   └── tkbeads/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       ├── app.py               # TkbeadsApp
│       │
│       ├── data/
│       │   ├── models.py        # Task, Status
│       │   ├── loader.py        # BeadsLoader
│       │   └── watcher.py       # FileWatcher
│       │
│       ├── store/
│       │   └── task_store.py    # TaskStore
│       │
│       ├── ui/
│       │   ├── screens/
│       │   │   └── kanban.py
│       │   ├── widgets/
│       │   │   ├── board.py
│       │   │   └── card.py
│       │   └── modals/
│       │       └── detail.py
│       │
│       └── styles/
│           └── app.tcss
```

## Зависимости

```toml
dependencies = [
    "textual>=0.89",
    "watchfiles>=0.24",
]
```

## Flow запуска

```
$ python -m tkbeads
       │
       ▼
find_beads_dir() ──► .beads/issues.jsonl
       │
       ▼
BeadsLoader.load() ──► [Task, Task, ...]
       │
       ▼
TaskStore.set_tasks() ──► UI рендерит KanbanScreen
       │
       ▼
FileWatcher.start() ──► ждёт изменений в фоне
       │
       ▼ (при изменении файла)
_reload_tasks() ──► UI обновляется
```

## Ссылки

- [Beads](https://github.com/steveyegge/beads) — оригинальный трекер
- [beads_viewer](https://github.com/Dicklesworthstone/beads_viewer) — Go TUI (референс)
- [Textual](https://textual.textualize.io/) — TUI-фреймворк
