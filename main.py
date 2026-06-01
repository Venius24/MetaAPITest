from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "my_super_secret_token_123"

# !!! СЮДА ВСТАВЬ ТОКЕН, КОТОРЫЙ СГЕНЕРИРОВАЛ В КОНСОЛИ META (ПунКТ 2) !!!
PAGE_ACCESS_TOKEN = "ТВОЙ_СГЕНЕРИРОВАННЫЙ_МАРКЕР_ДОСТУПА"

def send_message(recipient_id, text):
    """Функция отправки текстового сообщения через Instagram Graph API"""
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Ответ от Meta API: {response.status_code} - {response.text}")
    return response.json()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == "POST":
        data = request.json
        print(f"Получены данные: {data}")

        # Разбираем JSON от Meta и ищем текст сообщения
        try:
            if data.get("object") == "instagram":
                for entry in data.get("entry", []):
                    for messaging_event in entry.get("messaging", []):
                        # Проверяем, что это именно текстовое сообщение
                        if messaging_event.get("message") and not messaging_event["message"].get("is_echo"):
                            sender_id = messaging_event["sender"]["id"]  # ID того, кто написал
                            
                            print(f"Отправляем Pong пользователю {sender_id}...")
                            send_message(sender_id, "Pong")
                            
        except Exception as e:
            print(f"Ошибка при разборе сообщения: {e}")

        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    # Запускаем локально на 8082, Nginx перенаправит сюда
    app.run(host="127.0.0.1", port=8082)