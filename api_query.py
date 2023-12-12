import httpx
import ssl
from httpx._config import SSLConfig

async def send_feedback(feedback_data):
    url = "https://185.217.131.28:7000/feedback/"

    ssl_config = SSLConfig(verify=False, http2=True)

    async with httpx.AsyncClient(ssl=ssl_config) as client:
        response = await client.post(url, json=feedback_data)

    if response.status_code == 200:
        print("Запрос успешно отправлен")
        print(response.json())
    else:
        print(f"Ошибка при отправке запроса: {response.status_code}")
        print(response.text)