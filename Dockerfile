FROM python:3.13

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости через pip
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
