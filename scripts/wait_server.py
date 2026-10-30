# wait_server.py
import time
import requests

url = "http://127.0.0.1:8000/"
print("⏳ En attente que le serveur Django soit prêt...")

while True:
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print("✅ Serveur prêt !")
            break
    except requests.exceptions.ConnectionError:
        pass
    time.sleep(1)
