# SupplyFlow: веб-сервис управления поставками и заказами

SupplyFlow - курсовой проект веб-сервиса для оптовых компаний. Система помогает вести контрагентов, товары, складские остатки, заказы клиентов и поставки от поставщиков.

## Технологии

- Backend: Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, MongoDB, Redis
- Frontend: JavaScript, TypeScript, React, Tailwind CSS, Vite
- Infrastructure: Docker Compose, Nginx
- Архитектурный подход: MVC с выделением API-контроллеров, моделей, схем представления и сервисного слоя

## Быстрый запуск

```bash
docker compose up --build
```

После запуска:

- веб-интерфейс: http://localhost
- API: http://localhost/api
- Swagger: http://localhost/api/docs

## Демо в GitHub Codespaces

Проект можно показать прямо из GitHub без локальной установки Docker:

1. Откройте репозиторий на GitHub.
2. Нажмите `Code` -> `Codespaces` -> `Create codespace on main`.
3. Дождитесь запуска окружения. Docker Compose стартует автоматически.
4. Откройте вкладку `Ports` и перейдите по порту `8080`.

Если сервисы не стартовали автоматически, выполните в терминале Codespaces:

```bash
docker compose -f docker-compose.yml -f docker-compose.codespaces.yml up -d --build
```

Интерфейс будет доступен на forwarded-порту `8080`, API - на `8000`.

## Учетные записи

- Администратор: `admin` / `admin123`
- Оператор: `operator` / `operator123`

Администратор управляет справочниками и демо-данными. Оператор работает с заказами, поставками и складскими остатками.

## CI/CD

В проекте настроен GitHub Actions workflow `.github/workflows/ci-cd.yml`.

Pipeline выполняет:

- проверку `docker compose config`;
- сборку всех сервисов;
- запуск полного стека;
- smoke-тест `/api/health`;
- проверку входа администратора;
- публикацию Docker-образов в GitHub Container Registry при push в `main`.

Публикуемые образы:

- `ghcr.io/worldwide31/kr_backend-api:latest`
- `ghcr.io/worldwide31/kr_backend-frontend:latest`

## Production Compose

Для запуска из опубликованных образов:

```bash
cp .env.production.example .env.production
docker compose --env-file .env.production -f docker-compose.prod.yml up -d
```

Перед запуском замените пароли и `JWT_SECRET` в `.env.production`.

## Структура

```text
backend/app/api        HTTP-контроллеры FastAPI
backend/app/models     SQLAlchemy-модели предметной области
backend/app/schemas    Pydantic-схемы запросов и ответов
backend/app/services   бизнес-логика и интеграции с Redis/MongoDB
frontend/src/pages     страницы React-приложения
frontend/src/components общие UI-компоненты
docs                   материалы отчета и презентации
```

## Функциональность

- Dashboard с KPI по заказам, поставкам и складу
- CRUD для компаний, товаров, складов, заказов и поставок
- Автоматическое резервирование остатков при создании заказа
- Пополнение остатков при приемке поставки
- Журналирование ключевых операций в MongoDB
- Кэширование сводных показателей в Redis
- Nginx reverse proxy для фронтенда и API
