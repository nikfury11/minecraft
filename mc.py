import asyncio
import threading
import os

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8757261876:AAGuTtojcMVY6jnFo1_qcZGJizXLVbxYZQ0"

# ── Flask keepalive ─────────────────────────

app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Fallback bot is running."

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# ── Telegram bot ───────────────────────────

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" Server is offline.")

async def run_bot():
    while True:
        try:
            app = Application.builder().token(BOT_TOKEN).build()

            app.add_handler(CommandHandler("ping", ping))

            print("Fallback bot running...")
            await app.run_polling()

        except Exception as e:
            print("Main bot took over:", e)
            await asyncio.sleep(5)

# ── Main ───────────────────────────────────

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_bot())
