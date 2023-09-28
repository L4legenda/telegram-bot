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

usedCities = []

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    global usedCities
    f = open("russian-cities.json", "r", encoding='utf-8')
    russian_cities = f.read()
    f.close()
    rus_city = json.loads(russian_cities)
    message_user = update.message.text

    for city in rus_city:
        name_city = city['name']
        if name_city.lower() == message_user.lower():
            if message_user.lower() in usedCities:
                await update.message.reply_text("Город уже был")
                break
            usedCities.append(message_user.lower())
            last_char = message_user[-1]
            all_city_last_char = []
            for city in rus_city:
                if city['name'][0].lower() == last_char.lower():
                    all_city_last_char.append(city['name'])
            for i in range(100):
                random_city = random.choice(all_city_last_char)
                if random_city not in usedCities:
                    break
            usedCities.append(random_city.lower())
            await update.message.reply_text(random_city)
            break
    else:
        await update.message.reply_text("-")

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