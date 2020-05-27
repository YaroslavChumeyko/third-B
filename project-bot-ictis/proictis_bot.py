from telegram import Bot
from telegram.ext import Updater, Defaults

from config import TOKEN

import handlers

import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == "__main__":
    try:
        print("Started")

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
        dp = updater.dispatcher

        # Now bot'll know about handlers
        # dp.add_handler(handlers.filter_handler, group=0)
        dp.add_handler(handlers.info, group=1)
        # dp.add_handler(handlers.project_handler, group=1)
        dp.add_handler(handlers.greet_user, group=1)

        dp.add_error_handler(error)

        updater.start_polling()
        updater.idle()

    except KeyboardInterrupt:
        print('Finished')

