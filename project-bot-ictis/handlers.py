from telegram.ext import MessageHandler, Filters

from bot_filter import text_filter

from topics import topics


def sign_complete(update, bot):
    if update.message.text == 'Проект':
        bot.bot.send_message(
            chat_id=update.message.chat_id,
            text='Вы записаны'
        )


def project_sign(update, bot):
    text_message = update.message.text
    bot.bot.send_message(
        chat_id=update.message.chat_id,
        text='Выберите проект'
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=text_message
    )


def greetings(update, bot):
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"<i>Здравствуй</i>, { update.message.from_user.first_name }"
        )


filter_handler = MessageHandler(filters=Filters.text, callback=text_filter)

project_handler = MessageHandler(filters=Filters.regex('хочу записаться'), callback=project_sign)

greet_user = MessageHandler(filters=Filters.text(topics['greeting']), callback=greetings)

if __name__ == "__main__":
    pass