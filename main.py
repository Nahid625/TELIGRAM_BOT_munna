from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv

load_dotenv()




BOT_TOKEN = os.getenv("BOT_TOKEN")

# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-pro")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_message = update.message.text
#     response = model.generate_content(user_message)
#     await update.message.reply_text(response.text)
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm MCD and aur teri mkc 👋")

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()