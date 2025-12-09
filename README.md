
# IPCal Application

This is a Flask-based application for calculating and validating IPv4 and IPv6 addresses, subnets, and generating regex patterns for IP ranges.

## Features

- Calculate IPv4 and IPv6 details
- Convert CIDR to Netmask and vice versa
- Generate regex patterns for IP ranges
- Validate IPv4, IPv6, and subnet inputs

## Requirements

- Python 3.10
- Flask 2.0.2
- ipaddress 1.0.23
- MarkupSafe 2.1.1
- python-dotenv 0.19.2
- gunicorn 20.1.0

## Configuration

- Duplicate `.env.example` to `.env` and adjust values for your environment.
- `SECRET_KEY` **must** be set to a strong random value in production. The app will refuse to start without it when debug mode is off.
- `FLASK_DEBUG` should be `False` in production to avoid exposing sensitive information. If `SECRET_KEY` is missing in development mode, the app will generate a temporary key and log a warning; sessions will be reset when the process restarts.

## Installation

### Using Virtual Environment

1. Clone the repository:
    ```sh
    git clone https://github.com/ndlong78/ipcal.git
    cd ipcal
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Copy the sample environment file and update `SECRET_KEY` (and optionally `FLASK_DEBUG`):
    ```sh
    cp .env.example .env
    ```

6. Run the application:
    ```sh
    python3 run.py
    ```

### Using Docker

1. Ensure you have Docker and Docker Compose installed on your machine.

2. Clone the repository:
    ```sh
    git clone https://github.com/ndlong78/ipcal.git
    cd ipcal
    ```

3. Build the Docker image:
    ```sh
    docker-compose build
    ```

4. Run the Docker container:
    ```sh
    docker-compose up -d
    ```

5. Check Docker log:
    ```sh
    docker logs -f ipcal_web_1
    ```

6. Access the application by navigating to `http://localhost:5000` in your web browser.

## Removal

### Deactivate and Remove Application Folder

1. Stop Docker Compose from the `ipcal` folder:
    ```sh
    docker-compose down
    ```

2. Remove the application folder:
    ```sh
    rm -rf /path/to/ipcal
    ```

## Project Structure

```sh
ipcal/
├── app/
│   ├── __init__.py
│   ├── calculations.py
│   ├── ip_to_regex.py
│   ├── routes.py
│   └── templates/
│       └── index.html
│   └── static/
│       └── style.css
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── run.py

- **app/**: Contains the main application code.
  - `__init__.py`: Initializes the Flask application.
  - `calculations.py`: Contains calculation functions for IPv4, IPv6, and subnet details.
  - `ip_to_regex.py`: Contains functions to convert IP ranges to regex patterns.
  - `routes.py`: Defines the routes and logic for the application.
  - **templates/**: Contains HTML templates.
    - `index.html`: The main HTML template.
  - **static/**: Contains static files like CSS.
    - `style.css`: The main CSS file for styling.

- **requirements.txt**: Lists the Python dependencies.
- **Dockerfile**: Defines the Docker image for the application.
- **docker-compose.yml**: Defines the Docker services for the application.
- **.dockerignore**: Lists files and directories to be ignored by Docker.
- **run.py**: The main entry point to run the Flask application.

License
This project is licensed under the MIT License - see the LICENSE file for details.