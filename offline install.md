
### offline_install.md

```markdown
# Offline Installation Guide for IPCal Application

## Step 1: Create a list of required libraries
### Requirements

```sh
Flask==2.0.2
Werkzeug==2.0.0
ipaddress==1.0.23
MarkupSafe==2.1.1
python-dotenv==0.19.2
gunicorn==20.1.0
```

## Step 2: Download the Python packages into the packages directory

```sh
pip download -d ./packages -r requirements.txt
```

## Step 3: Edit the Dockerfile

```Dockerfile
# Use Python slim image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the downloaded packages into the /packages directory in the image
COPY packages /packages

# Copy the requirements.txt file into the image
COPY requirements.txt requirements.txt

# Install the packages from the /packages directory
RUN pip install --no-cache-dir --no-index --find-links=/packages -r requirements.txt

# Copy the entire application source code into the image
COPY . .

# Set default environment variables
ENV GUNICORN_WORKERS=4

# Use CMD to run Gunicorn with the correct module and settings
CMD ["gunicorn", "--workers", "${GUNICORN_WORKERS}", "--bind", "0.0.0.0:8000", "app:app"]
```

## Step 4: Build the Docker image and check logs

```sh
docker-compose up --build -d
docker logs -f ipcal_web_1
```
```
