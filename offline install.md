
#Bước 1: Tạo danh sách thư viện cần thiết
## Requirements

```sh

Flask==2.0.2
Werkzeug==2.0.0
ipaddress==1.0.23
MarkupSafe==2.1.1
python-dotenv==0.19.2
gunicorn==20.1.0

```
#Bước 2: Tải xuống các gói Python vào thư mục packages

```sh
pip download -d ./packages -r requirements.txt

```
#Bước 4: Chỉnh sửa file  Dockerfile

```sh

# Sử dụng image Python slim làm base
FROM python:3.10-slim

# Đặt thư mục làm việc
WORKDIR /app

# Copy các gói đã tải về vào thư mục /packages trong image
COPY packages /packages

# Copy file requirements.txt vào image
COPY requirements.txt requirements.txt

# Cài đặt các gói từ thư mục /packages
RUN pip install --no-cache-dir --no-index --find-links=/packages -r requirements.txt

# Copy toàn bộ mã nguồn của ứng dụng vào image
COPY . .

# Đặt biến môi trường mặc định
ENV GUNICORN_WORKERS=4

# Sử dụng lệnh CMD để chạy Gunicorn với module và thuộc tính đúng
CMD ["gunicorn", "--workers", "${GUNICORN_WORKERS}", "--bind", "0.0.0.0:8000", "app:app"]

```

#Bước 5: Xây dựng và Docker image và kiểm tra log

```sh
docker-compose up --build -d
docker logs -f  ipcal_web_1

```