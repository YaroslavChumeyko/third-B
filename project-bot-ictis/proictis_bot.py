from telegram import Bot
from telegram.ext import Updater, Defaults

from config import TOKEN

import handlers

import logging

if __name__ == "__main__":
    print("Started")
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    proictis_bot = Bot(
        token=TOKEN,
        defaults=Defaults(
            parse_mode="HTML",
        ),
    )
    updater = Updater(
        bot=proictis_bot,
        use_context=True
    )

    updater.dispatcher.add_handler(handlers.filter_handler, group=0)
    updater.dispatcher.add_handler(handlers.project_handler, group=1)
    updater.dispatcher.add_handler(handlers.greet_user, group=1)

    updater.start_polling()
    updater.idle()

