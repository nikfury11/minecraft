import os
import time
import asyncio
import threading

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8757261876:AAGuTtojcMVY6jnFo1_qcZGJizXLVbxYZQ0"

# ── Flask ──────────────────────────────────

web = Flask(__name__)

@web.route("/")
def home():
    return "Fallback bot running."

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# ── Telegram ───────────────────────────────

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔴 Server is offline.")

# ── Bot loop ───────────────────────────────

async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("ping", ping))

    print("Fallback bot connected.")

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

    # keep alive forever
    await asyncio.Event().wait()

# ── Retry forever ──────────────────────────

while True:
    try:
        asyncio.run(run_bot())

    except Exception as e:
        print(f"Main bot probably active: {e}")

        time.sleep(5)
