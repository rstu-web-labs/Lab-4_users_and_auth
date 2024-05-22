### последовательность выполнения команд для успешного запуска
+ заполнить файл .env 
```
cp .example.env .env
```
+ для локальной работы запустить
```
docker-compose --env-file .env -f infra/docker-compose.local.yaml up --build
```
+ развернуть сервис в режиме тестирования или Продакшн:
```
docker-compose --env-file .env -f infra/docker-compose.yaml up
```