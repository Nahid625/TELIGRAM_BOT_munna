# for update data
from telegram import Update 
# for build aplicaton and handle command and other things 
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler,filters, ContextTypes
# langchain plus grok import
from langchain_groq import ChatGroq 
from langchain_core.messages import HumanMessage,AIMessage

# import os and env
import os
from dotenv import load_dotenv

# load env
load_dotenv()


# get api key secrate from env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_SECRATE = os.getenv("GROQ_API_SECRATE")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# setup llmm main brain who could predict next word
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)
# ram memory use
users_sessions = {}
# get history 
def get_history(user_id):
    if user_id not in users_sessions:
        users_sessions[user_id]=[]
    return users_sessions[user_id]


async def start(update : Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hallow im your assistance that made by Junior Dev Nahid From chuidarland"
  #  print(context.user_data)
    )


async def clear(update : Update, context : ContextTypes.DEFAULT_TYPE):
    # get user id 
    user_id = update.message.from_user.id
    if user_id in users_sessions:
        del users_sessions[user_id]
    await update.message.reply_text("memory cleard Fresh start")



# ai response handler 
async def ai_reply(update : Update, context : ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # get user message
    user_message = update.message.text
    await update.message.chat.send_action("typing kortesi mcd...")
    # get history
    history = get_history(user_id)
    # add human sms to history 
    history.append(HumanMessage(content= user_message))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))
    await update.message.reply_text(response.content)



app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("clear", clear))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    
app.run_polling()