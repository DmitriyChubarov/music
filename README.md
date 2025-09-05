# Music API Service

## Возможности:
- Все эндпоинты доступны для просмотра и тестирования через Swagger UI по адресу: http://127.0.0.1:8000/api/swagger/

### Технологии

- Python 3 / Django 5
- PostgreSQL
- Docker, Docker Compose

### Установка и запуск

Открываем терминал, создаём папку, в которой будет располагаться проект и переходим в неё:
```bash
mkdir /ваш/путь
cd /ваш/путь
```
Клонируем репозотирий в эту папку, переходим в папку проекта:
```bash 
git clone https://github.com/DmitriyChubarov/music.git
cd music
```
Запускаем Docker на устройстве, после чего собираем Docker образ и запускаем сервис:
```bash
docker compose build
docker compose up
```
Открываем новое окно терминала, переходим в папку проекта, применяем миграции, создаём суперпользователя и запускаем тесты:
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test
```
Сервисом можно пользоваться, удачи!

*Если все прошло успешно, но сервис не работает, прописать в терминале:
```bash
docker compose restart web
```
  
### Контакты
- tg: @eeezz_z
- gh: https://github.com/DmitriyChubarov
