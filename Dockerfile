# Берем официальный легкий образ питона
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем зависимости и устанавливаем их (для кэширования Докером)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код
COPY . .

# Команда для запуска нашего сервера
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]