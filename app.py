python
import os
TOKEN= os.getenv('TELEGRAM_BOT_TOKEN')
python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Estou vivo! Robot Trader Vision operando."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Antes de iniciar o bot do Telegram, chame:
keep_alive()
# ... aqui segue o código de iniciar o bot ...
