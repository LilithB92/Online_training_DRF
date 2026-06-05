FROM python:3.13

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости через pip
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
