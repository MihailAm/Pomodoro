# перед всеми командами надо ввести: mingw32-make
install-lib:
	pip install $(lib)

# Удаление указанной библиотеки
uninstall-lib:
	pip uninstall -y $(lib)

# Создание файла requirements.txt
freeze:
	pip freeze > requirements.txt

# Запуск FastAPI проекта на порту 8000
run:
	uvicorn main:app --reload

# Создать миграции
make-migrate:
	alembic revision --autogenerate -m $(MIGRATE)

# Применить миграции
migrate:
	alembic upgrade head