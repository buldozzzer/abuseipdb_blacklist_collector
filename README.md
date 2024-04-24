# Модуль актуализации локальной базы "грязных" IP-адресов с сервиса AbuseIPDB

Настоящий модуль предствляет собой очередь задач.

## Настройка

1. Создать аккаунты на сервисе [AbuseIPDB](https://www.abuseipdb.com/) и выпустить токен для каждого из созданных аккаунтов. 
API позволяет получать черный список 5 раз в день для каждого аккаунта. 
Таким образом, чем больше создано аккаунтов, тем чаще будет актуализироваться локальная база "грязных" IP-адресов.
По опыту, 3х - аккаунтов достаточно.

2. Переименовать файл example.config.ini в config.ini и заполнить его в соответствии с комментариями в файле.

## Запуск сервиса

Для хранения данных потребуется СУБД [ClickHouse](https://clickhouse.com/docs/ru/getting-started/install).

### Локально

Для работы очереди трубуется СУБД Redis. Установите ее или разверните ее в докер-контейнере, например, так:

```
docker run -d -p 6379:6379 redis
``` 

Запуск очереди:

```
poetry run celery -A abuseipdb.main worker -B
```

### Docker-compose

При запуске в Docker дополнительно устанавливать Redis **не нужно**.

Перед запском отредактиируйте файл __docker-compose.yml__.

```
docker compose up -d
```
