import time
import requests

# Your deployed Render URL
URL = "https://ai-me-backend.onrender.com/ping"


def ping():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            print(f"[{time.ctime()}] Ping successful: {response.json()}")
        else:
            print(
                f"[{time.ctime()}] Ping failed: Status code {response.status_code}")
    except Exception as e:
        print(f"[{time.ctime()}] Ping error: {e}")


if __name__ == "__main__":
    while True:
        ping()
        time.sleep(600)  # Ping every 10 minutes
