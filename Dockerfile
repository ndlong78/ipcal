FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Đặt biến môi trường mặc định
ENV GUNICORN_WORKERS=4

# Sử dụng lệnh CMD để chạy Gunicorn với module và thuộc tính đúng
CMD ["gunicorn", "--workers", "${GUNICORN_WORKERS}", "--bind", "0.0.0.0:8000", "app:app"]