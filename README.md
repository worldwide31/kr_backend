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

