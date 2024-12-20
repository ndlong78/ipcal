# IPv4, Subnet, Regex Calculator

This project is a simple Flask application that calculates IPv4 details, networks, subnets, and generates regex patterns for IP ranges.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ndlong78/ipcal.git
    cd ipcal
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python run.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Enter an IPv4 address and network (CIDR or IP + Netmask) to calculate the details.

## License

This project is licensed under the MIT License.


## Quick install to /otp
```sh

cd /opt
rm -rf ipcal/
git clone https://github.com/ndlong78/ipcal.git
cd /opt/ipcal

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 run.py

```