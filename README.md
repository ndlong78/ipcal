# IPCal Application

This is a Flask-based application for calculating and validating IPv4 addresses, subnets, and generating regex patterns for IP ranges.

## Features

- Calculate IPv4 details
- Convert CIDR to Netmask and vice versa
- Generate regex patterns for IP ranges
- Validate IPv4 and subnet inputs

## Requirements

- Python 3.10
- Flask 2.0.2
- ipaddress 1.0.23

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

5. Run the application:
    ```sh
    python run.py
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
    docker-compose up
    ```

5. Access the application by navigating to `http://localhost:5000` in your web browser.

## Project Structure
<<<<<<< HEAD
    ```sh

=======
```sh
>>>>>>> 9745d56c56789bb936dfddcaa60a907b7a32cb42
/opt/ipcal
├── app
│ ├── init.py
│ ├── calculations.py
│ ├── ip_to_regex.py
│ ├── routes.py
│ └── templates
│   └── index.html
│ └── static
│   └── style.css
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── run.py

- **app/**: Contains the main application code.
  - `__init__.py`: Initializes the Flask application.
  - `calculations.py`: Contains calculation functions for IPv4 and subnet details.
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
<<<<<<< HEAD
    
    ```
=======
```
>>>>>>> 9745d56c56789bb936dfddcaa60a907b7a32cb42
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
