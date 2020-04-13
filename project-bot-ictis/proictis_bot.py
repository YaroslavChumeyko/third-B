from telegram import Bot
from telegram.ext import Updater

from config import TOKEN

from handlers import text_handler

import logging


def main():
    print("Started")
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    proictis_bot = Bot(
        token=TOKEN
    )
    updater = Updater(
        bot=proictis_bot,
        use_context=True
    )

    updater.dispatcher.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
