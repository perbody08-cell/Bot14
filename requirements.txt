FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Добавляем /app в PYTHONPATH чтобы Python видел пакеты
ENV PYTHONPATH=/app

CMD ["python", "main.py"]
