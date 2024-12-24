FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Đặt biến môi trường mặc định
ENV GUNICORN_WORKERS=4

# Sử dụng entrypoint để chạy Gunicorn với biến môi trường
CMD ["gunicorn", "--workers", "${GUNICORN_WORKERS}", "app:app"]