# Sử dụng image Python chính thức
FROM python:3.10-slim

# Đặt biến môi trường để đảm bảo các đầu vào không bị hỏi trong quá trình cài đặt
ENV PYTHONUNBUFFERED 1

# Tạo thư mục làm việc
WORKDIR /app

# Sao chép các tệp yêu cầu vào thư mục làm việc
COPY requirements.txt /app/

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . /app/

# Chạy ứng dụng
CMD ["python3", "run.py"]