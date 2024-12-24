To configure Nginx as a proxy for the `ipcal` application with the domain `ipcal.domain.com`, follow these steps:

1. **Install Nginx**: If Nginx is not installed, you can install it using the following commands:

    On Ubuntu:
    ```sh
    sudo apt update
    sudo apt install nginx
    ```

    On CentOS:
    ```sh
    sudo yum install epel-release
    sudo yum install nginx
    ```

2. **Configure Nginx**: Create a new configuration file for the domain `ipcal.domain.com`.

    Open the Nginx configuration file:
    ```sh
    sudo nano /etc/nginx/sites-available/ipcal
    ```

    Add the following content to the configuration file:
    ```nginx
    server {
        listen 80;
        server_name ipcal.domain.com;

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

    **Explanation of the configuration:**
    - `listen 80;`: Listen on port 80 (HTTP).
    - `server_name ipcal.domain.com;`: Define the server name for this domain.
    - `location / { ... }`: Define the proxy settings to forward all requests to `http://127.0.0.1:5000` (where the `ipcal` application is running).

3. **Enable the Nginx Configuration**: Create a symbolic link from `sites-available` to `sites-enabled` and restart Nginx.

    ```sh
    sudo ln -s /etc/nginx/sites-available/ipcal /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

4. **Configure Firewall (if necessary)**: Ensure that ports 80 (HTTP) and 443 (HTTPS) are open on your firewall.

    On Ubuntu:
    ```sh
    sudo ufw allow 'Nginx Full'
    ```

    On CentOS:
    ```sh
    sudo firewall-cmd --permanent --zone=public --add-service=http
    sudo firewall-cmd --permanent --zone=public --add-service=https
    sudo firewall-cmd --reload
    ```

5. **Set Up SSL Certificates (optional)**: To secure your connection, you can set up SSL certificates using Let's Encrypt.

    On Ubuntu:
    ```sh
    sudo apt update
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d ipcal.domain.com
    ```

    On CentOS:
    ```sh
    sudo yum install certbot python3-certbot-nginx
    sudo certbot --nginx -d ipcal.domain.com
    ```

    Certbot will automatically configure SSL for Nginx and set up automatic certificate renewal.

6. **Verify Configuration**: Ensure that Nginx is running properly and is proxying requests to the `ipcal` application.

    ```sh
    sudo systemctl status nginx
    ```

Now you can access the `ipcal` application via the domain `http://ipcal.domain.com`. If SSL is configured, access it via `https://ipcal.domain.com`.

If you encounter any issues during the configuration process, check the Nginx logs for more information:
```sh
sudo tail -f /var/log/nginx/error.log
```

