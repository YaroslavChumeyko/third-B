from telegram.ext import MessageHandler, Filters


def text_reply(update, bot):
    text_message = update.message.text
    greet_list = ['привет', 'здравствуй', 'хеллоу']
    for greeting in greet_list:
        if greeting in text_message.lower():
            return greetings(update, bot)
        else:
            return bot.bot.sendMessage(chat_id=update.message.chat_id, text=text_message)


def greetings(update, bot):
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"Здравствуй, { update.message.from_user.first_name }"
        )


text_handler = MessageHandler(Filters.text, text_reply)
