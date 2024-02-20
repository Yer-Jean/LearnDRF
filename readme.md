## Создание и запуск контейнеров Docker
### Требования
Необходимо на хост-компьютере установить Docker для необходимой платформы, скачав его по адресу https://docs.docker.com/get-docker/

### Запуск
- Собрать образ вводом в окне Терминала команды: docker-compose build
- В другом окне Терминала создать базу данных:
  - Ввести команду: psql -U postgres
  - Далее в оболочке Postgres выполнить команду: CREATE DATABASE learn_drf;
  - Выйти из оболочки вводом команды: \q
- В этом же окне Терминала применить миграции к созданной базе данных введя команду: docker-compose exec app python manage.py migrate
- В начальном окне Терминала запустить контейнеры командой: docker-compose up
- (Перед этими шагами, возможно, понадобится экспортировать зависимости из файла pyproject.toml в файл requirements.txt введя команду: poetry export -f requirements.txt --output requirements.txt)