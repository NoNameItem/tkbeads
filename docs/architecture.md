# Архитектура tkbeads

tkbeads — TUI-приложение для [Beads](https://github.com/steveyegge/beads) task tracker, построенное на Textual.

## Трёхслойная архитектура

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

## Поток данных

**Чтение:**
```
FileWatcher → BeadsLoader → TaskStore → UI обновляется
```

**Запись:**
```
UI action → TaskStore.update_status() → BeadsLoader.save() → файл обновлён
```

## Компоненты

### Data Layer

- **BeadsLoader** — чтение/запись `.beads/issues.jsonl`
- **FileWatcher** — отслеживание изменений файла для live updates
- **Task, Status** — доменные модели

### State Layer

- **TaskStore** — централизованное хранилище задач с reactive-обновлениями
- Логика распределения по колонкам (blocked/ready/in_progress/closed)
- Построение дерева parent-child

### UI Layer

- **KanbanScreen** — основной экран с 4 колонками
- **TaskCard** — карточка задачи
- **TaskDetailModal** — модалка с деталями и сменой статуса

## Логика колонок

| Колонка | Условие |
|---------|---------|
| BLOCKED | `status == open` И есть открытые блокеры |
| READY | `status == open` И нет открытых блокеров |
| IN PROGRESS | `status == in_progress` |
| CLOSED | `status == closed` |

## Иерархия задач

Задачи связаны через `parent_id`. Дети отображаются:
- С отступом под родителем в той же колонке
- С цепочкой предков (dimmed) если находятся в другой колонке

## Структура проекта

```
src/tkbeads/
├── __main__.py          # Entry point
├── app.py               # TkbeadsApp
├── data/
│   ├── models.py        # Task, Status
│   ├── loader.py        # BeadsLoader
│   └── watcher.py       # FileWatcher
├── store/
│   └── task_store.py    # TaskStore
├── ui/
│   ├── screens/kanban.py
│   ├── widgets/board.py, card.py
│   └── modals/detail.py
└── styles/app.tcss
```
