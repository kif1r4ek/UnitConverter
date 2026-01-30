# Docker Setup для Unit Converter

## Быстрый старт

### 1. Подготовка окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

### 2. Запуск всех сервисов

```bash
docker-compose up -d
```

Эта команда запустит:
- FastAPI приложение на `http://localhost:8000`
- Redis на порту `6379`
- Redis Commander (GUI) на `http://localhost:8081`

### 3. Проверка статуса сервисов

```bash
docker-compose ps
```

### 4. Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Только приложение
docker-compose logs -f app

# Только Redis
docker-compose logs -f redis
```

## Команды Docker Compose

### Остановка сервисов

```bash
docker-compose down
```

### Остановка с удалением volumes (очистка данных Redis)

```bash
docker-compose down -v
```

### Пересборка образов

```bash
docker-compose build

# Пересборка без кеша
docker-compose build --no-cache
```

### Перезапуск отдельного сервиса

```bash
docker-compose restart app
docker-compose restart redis
```

## Доступ к сервисам

- **Приложение**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **Redis Commander**: http://localhost:8081

## Локальная разработка с Docker

### Hot Reload

Приложение настроено на автоматическую перезагрузку при изменении кода благодаря volume mapping в `docker-compose.yml`.

### Выполнение команд внутри контейнера

```bash
# Войти в bash контейнера приложения
docker-compose exec app bash

# Запустить тесты
docker-compose exec app pytest

# Проверить подключение к Redis
docker-compose exec redis redis-cli ping
```

## Работа с Redis

### Подключение через redis-cli

```bash
docker-compose exec redis redis-cli
```

### Базовые команды Redis

```redis
# Установить значение
SET mykey "Hello"

# Получить значение
GET mykey

# Проверить все ключи
KEYS *

# Удалить ключ
DEL mykey
```

### Использование Redis Commander

Откройте http://localhost:8081 в браузере для графического интерфейса управления Redis.

## Персистентность данных

Данные Redis сохраняются в Docker volume `redis_data`. При остановке и повторном запуске контейнеров данные сохраняются.

Для полной очистки данных:

```bash
docker-compose down -v
```

## Логи приложения

Логи сохраняются в директорию `./logs` на хосте:
- `app.log` - все логи приложения (INFO и выше)
- `error.log` - только ошибки (ERROR и выше)

## Production Deploy

Для production окружения:

1. Измените `.env`:
   - Установите `DEBUG=False`
   - Установите `LOG_LEVEL=WARNING`
   - Установите `LOG_FORMAT=json`
   - Добавьте `REDIS_PASSWORD`

2. Обновите `docker-compose.yml`:
   - Удалите volume mapping для кода (строку `- .:/app`)
   - Удалите Redis Commander
   - Настройте ресурсные лимиты

3. Используйте отдельный файл для production:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Redis не запускается

Проверьте, не занят ли порт 6379:

```bash
lsof -i :6379
```

### Приложение не может подключиться к Redis

1. Проверьте, что Redis контейнер запущен:
   ```bash
   docker-compose ps redis
   ```

2. Проверьте логи Redis:
   ```bash
   docker-compose logs redis
   ```

3. Проверьте сетевое подключение:
   ```bash
   docker-compose exec app ping redis
   ```

### Ошибки при сборке

Очистите Docker кеш и пересоберите:

```bash
docker system prune -a
docker-compose build --no-cache
```

## Мониторинг

### Статистика контейнеров

```bash
docker stats
```

### Использование Redis памяти

```bash
docker-compose exec redis redis-cli INFO memory
```

## Остановка и очистка

```bash
# Остановка без удаления
docker-compose stop

# Полная остановка с удалением контейнеров
docker-compose down

# Удаление с volumes и images
docker-compose down -v --rmi all
```