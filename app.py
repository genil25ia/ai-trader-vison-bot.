import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- CONFIGURAÇÃO DE LOG ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("BotTrader")

# --- VARIÁVEIS DE AMBIENTE ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- KEEP ALIVE PARA O RAILWAY ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 AI Trader Vision Bot está ONLINE e operando!"

def run_http():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_http)
    t.start()


# -----------------------------
#        FUNÇÕES DO BOT
# -----------------------------

async def comecar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""

    # Verifica acesso (opcional)
    if CHAT_ID and str(update.message.chat.id) != CHAT_ID:
        logger.info(f"Acesso NÃO autorizado do chat: {update.message.chat.id}")
        await update.message.reply_text("Acesso negado.")
        return

    await update.message.reply_text(
        "Olá! Sou o AI Trader Vision Bot.\n"
        "Estou monitorando e conectado ao servidor."
    )

    await update.message.reply_text(
        f"Recebi sua mensagem: {update.message.text}"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde qualquer texto"""
    if CHAT_ID and str(update.message.chat.id) != CHAT_ID:
        return

    await update.message.reply_text(f"Recebi sua mensagem: {update.message.text}")


# -----------------------------
#          MAIN
# -----------------------------

def main():
    """Inicia o bot"""
    if not TOKEN:
        logger.error("ERRO: A variável TELEGRAM_BOT_TOKEN não foi encontrada.")
        return

    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", comecar))

    # Resposta para textos
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot iniciado. Aguardando comandos...")

    application.run_polling()


# -----------------------------
#      EXECUÇÃO PRINCIPAL
# -----------------------------

if __name__ == '__main__':
    keep_alive()   # servidor web para o Railway
    main()         # inicia o bot
