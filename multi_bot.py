import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import json

import random

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

multi = ""

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global multi
    if multi == "bot_ai":
        bot_ai(update, context)
    if multi == "bot_city":
        bot_city(update, context)
    if update.message.text == "Презентация":
        multi = "bot_ai"
    if update.message.text == "Города":
        multi = "bot_city"


async def bot_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

def gtp_async(obj):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "user", "content": "Создай презентацию на 8 слайдов с загаловком и описанием"},
            {"role": "user", "content": obj['message']}
        ],
        stream=True,
    )
    message = ''.join([i for i in response])
    obj['result'] = message
    print(message)

async def bot_ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    obj = {
        "message": update.message.text,
        "result": ""
    }
    t = threading.Thread(target=gtp_async, args=(obj,))
    t.start()
    t.join()

    await update.message.reply_text(obj['result'])

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6528022690:AAGH6SxoSxn0KHNQQ_Wpsf521V7ID4lCh8o").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()