from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# LangChain + Groq imports
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Setup LangChain + Groq
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

# Memory per user (stores chat history)
user_sessions = {}

def get_history(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    return user_sessions[user_id]


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Im Munna The Ultra tipe Of khoniker pola \nPowered by Lawra AI + LangChain with Python!\nAsk me anything!"
    )

# /clear command - resets conversation memory
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
    await update.message.reply_text("Memory cleared! Fresh start ")

# AI response handler
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    await update.message.chat.send_action("typing")  # shows "typing..." in chat

    history = get_history(user_id)
    history.append(HumanMessage(content=user_message))

    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))

    await update.message.reply_text(response.content)


# Build app
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

app.run_polling()