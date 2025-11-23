import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURAÇÃO DE LOG (Para ver erros no Railway) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

# --- VARIÁVEIS DE AMBIENTE ---
# O Railway vai injetar esses valores. Se rodar local, ele avisa que falta.
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- PARTE 1: O "TRUQUE" DO KEEP ALIVE (SERVIDOR WEB) ---
app = Flask('')

@app.route('/')
def home():
    return "🤖 AI Trader Vision Bot está ONLINE e operando!"

def run_http():
    # O Railway define a porta automaticamente na variável PORT, ou usa 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# --- PARTE 2: LÓGICA DO BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde ao comando /start"""
    await update.message.reply_text(
        "Olá! Sou o AI Trader Vision Bot. 🚀\n"
        "Estou monitorando o mercado e conectado ao servidor."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """(Opcional) Responde qualquer mensagem de texto para testar"""
    await update.message.reply_text(f"Recebi sua mensagem: {update.message.text}")

# AQUI VOCÊ PODE COLOCAR SUA LÓGICA DE ANÁLISE DE IMAGEM / OPENAI
# Se você tiver a função de análise pronta, adicione ela aqui e crie um Handler.

def main():
    """Inicia o bot"""
    if not TOKEN:
        print("ERRO: A variável TELEGRAM_BOT_TOKEN não foi encontrada.")
        return

    # Cria a aplicação
    application = Application.builder().token(TOKEN).build()

    # Adiciona os comandos
    application.add_handler(CommandHandler("start", start))
    # Opcional: responde a textos comuns
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Inicia o Bot
    print("Bot iniciado...")
    application.run_polling()

if name == 'main':
    # 1. Inicia o servidor web em segundo plano (para o UptimeRobot)
    keep_alive()
    # 2. Inicia o bot do Telegram (Bloqueia o código aqui para rodar o loop)
    main()
