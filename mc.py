import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" Server is offline.")

async def main():
    while True:
        try:
            app = Application.builder().token(BOT_TOKEN).build()

            app.add_handler(CommandHandler("ping", ping))

            print("Fallback bot running...")
            await app.run_polling()

        except Exception as e:
            print("Main bot probably took over:", e)

            await asyncio.sleep(5)

asyncio.run(main())
