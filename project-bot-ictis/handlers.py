from telegram.ext import MessageHandler, \
    ConversationHandler, CommandHandler, Filters

from bot_filter import text_filter

from topics import topics

import site_logic


FIND = 0


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


def exit_command(update, bot):
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text="<i>Понял-принял</i>, прерываю текущее действие"
    )
    return ConversationHandler.END


def mentors_call(update, bot):
    bot_message = site_logic.mentors_names()
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_message
    )
    return FIND


def mentor_find(update, bot):
    user_message = update.message.text
    if user_message == 'выход':
        return exit_command(update, bot)
    name = update.message.text
    bot_answer = site_logic.one_mentor(name)
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_answer
    )
    return FIND


filter_handler = MessageHandler(filters=Filters.text, callback=text_filter)

project_handler = MessageHandler(filters=Filters.regex('хочу записаться'), callback=project_sign)

greet_user = MessageHandler(filters=Filters.text(topics['greeting']), callback=greetings)

# mentors_info = MessageHandler(filters=Filters.text, callback=mentor_find)
mentors = ConversationHandler(
    entry_points=[CommandHandler(command='mentors', callback=mentors_call)],
    states={
        FIND: [MessageHandler(filters=Filters.text, callback=mentor_find)]
    },
    fallbacks=[
        CommandHandler(command='exit', callback=exit_command),
        MessageHandler(filters=Filters.text(["выход"]), callback=exit_command)
    ]
)

if __name__ == "__main__":
    pass