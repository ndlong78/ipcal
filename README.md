This is a ip address calculate base on FLASK and Python3

cd /opt

git clone https://github.com/ndlong78/ipcal.git

cd /opt/ipcal

source venv/bin/activate

chmod -R 755 templates/

chmod -R 755 static/

chmod 644 templates/index.html

chmod 644 static/style.css

python3 run.py
