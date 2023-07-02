import os
import logging
from telegram.ext import Application
from handlers import getMessageHandlers, getCommandHandlers, getCallbackQueryHandlers
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logger = logging.getLogger(__name__)


def main():

    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    for handler in getCommandHandlers() + getMessageHandlers() + getCallbackQueryHandlers():
        application.add_handler(handler)

    application.run_polling()    


if __name__ == "__main__":
    main()
