from flask import Flask, request, jsonify

app = Flask(__name__)

# Тот самый токен, который ты придумаешь и вставишь в консоли
VERIFY_TOKEN = "my_super_secret_token_123"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Это нужно для подтверждения URL в Facebook Developers
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == "POST":
        # Сюда будут приходить сообщения от пользователей
        data = request.json
        print(f"Получены данные: {data}")
        # Здесь будет логика обработки сообщений
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(port=8082)