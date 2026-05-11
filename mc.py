import os
import time
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

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

# ── Retry loop ─────────────────────────────
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ping", ping))
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    print("Fallback bot connected.")

    # Keep running until an exception kills the polling
    while True:
        await asyncio.sleep(1)

    await app.updater.stop()
    await app.stop()
    await app.shutdown()

while True:
    try:
        asyncio.run(run_bot())  # fresh event loop every attempt
    except Exception as e:
        print(f"Main bot probably active ({type(e).__name__}: {e}), retrying in 5s...")
        time.sleep(5)
