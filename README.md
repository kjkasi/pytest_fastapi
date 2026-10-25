# FastAPI repository demo

Небольшое демонстрационное приложение с:

- FastAPI-роутером для CRUD операций над задачами;
- SQLAlchemy 2.x repository;
- SQLite по умолчанию (`./demo.db`);
- dependency injection для подмены repository в тестах;
- unit-тестами роутеров и repository без подключения к базе данных.

## Запуск

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1

python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

После запуска документация доступна по адресу <http://127.0.0.1:8000/docs>.

Таблицы создаются при старте приложения. URL базы можно изменить переменной окружения:

```bash
DATABASE_URL=sqlite:///./local.db uvicorn app.main:app --reload
```

## Тесты

```bash
pytest
```

Тесты намеренно не используют SQLite:

- `tests/test_task_router.py` подменяет `get_task_repository` на `Mock`; роутер проверяется через `TestClient`;
- `tests/test_task_repository.py` передаёт repository `MagicMock(spec=Session)` и проверяет вызовы `get`, `add`, `commit`, `refresh`, `delete`;
- `create_app(initialize_database=False)` отключает lifespan-инициализацию БД в тестах.

## Структура

```text
app/
  database.py          # engine, Session и dependency get_db
  dependencies.py      # FastAPI dependency для TaskRepository
  main.py              # app factory и lifespan
  models.py            # SQLAlchemy-модель Task
  schemas.py           # Pydantic-схемы API
  repositories/
    tasks.py           # слой работы с Session
  routers/
    tasks.py           # HTTP endpoints

tests/
  test_task_repository.py
  test_task_router.py
```
