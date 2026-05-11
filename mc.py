import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8577565701:AAExAi7fzDcth664HhRq4X4PNNloYuZm6HM"

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

# ── Main ───────────────────────────────────
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("ping", ping))

print("Fallback bot connected.")
app.run_polling(drop_pending_updates=True)  # removed close_loop=False
