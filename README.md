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

## Remove

### Deactivate and remove application folder

### Stop docker-compose from ipcal folder 

```sh
    docker-compose down