from telegram.ext import MessageHandler, \
    ConversationHandler, CommandHandler, Filters

from bot_filter import text_filter

import bot_topics

import site_logic


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


# functions based on site information
def do_mentors(update, bot):
    bot_message = site_logic.find_info(
        'mentors',
        bot_topics.mentors_info,
        'name'
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_message
    )
    # for key in bot_topics.mentors_info.keys():
    #     bot_topics.mentors_info[key] = []
    return MENTORS


def do_news(update, bot):
    bot_message = site_logic.find_info(
        'news',
        bot_topics.news_info,
        'title'
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_message
    )
    # for key in bot_topics.news_info.keys():
    #     bot_topics.news_info[key] = []
    return MENTORS


def do_achievements(update, bot):
    bot_message = site_logic.find_info(
        'achievements',
        bot_topics.achievements_info,
        'title'
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_message
    )
    # Clear "mentors_info" for next usage
    # for key in bot_topics.achievements_info.keys():
    #     bot_topics.achievements_info[key] = []
    return MENTORS


def do_competitions(update, bot):
    bot_message = site_logic.find_info(
        'competitions',
        bot_topics.competitions_info,
        'name'
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_message
    )
    # for key in bot_topics.competitions_info.keys():
    #     bot_topics.competitions_info[key] = []
    return MENTORS


def mentor_find(update, bot):
    user_message = update.message.text
    if user_message == 'выход':
        return exit_command(update, bot)
    name = update.message.text
    bot_answer = site_logic.one_mentor(
        name,
        site_logic.url_path['mentors'],
        bot_topics.mentors_info
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_answer
    )
    return MENTORS


filter_handler = MessageHandler(filters=Filters.text, callback=text_filter)
project_handler = MessageHandler(filters=Filters.regex('хочу записаться'), callback=project_sign)
greet_user = MessageHandler(filters=Filters.text(bot_topics.topics['greeting']), callback=greetings)

# Non-database information from site
MENTORS, NEWS, ACHIEVEMENTS, COMPETITIONS = range(4)
info = ConversationHandler(
    entry_points=[
        # mentors
        CommandHandler(command='mentors', callback=do_mentors),
        MessageHandler(filters=Filters.regex('наставники'), callback=do_mentors),
        # news
        CommandHandler(command='news', callback=do_news),
        MessageHandler(filters=Filters.regex('новости'), callback=do_news),
        # news
        CommandHandler(command='achieves', callback=do_achievements),
        MessageHandler(filters=Filters.regex('достижения'), callback=do_achievements),
        # news
        CommandHandler(command='contests', callback=do_competitions),
        MessageHandler(filters=Filters.regex('конкурсы'), callback=do_competitions),
    ],
    states={
        # show mentor
        MENTORS: [MessageHandler(filters=Filters.text, callback=mentor_find)],
        # show news
        NEWS: [MessageHandler(filters=Filters.text, callback=mentor_find)],
        # show achievement
        ACHIEVEMENTS: [MessageHandler(filters=Filters.text, callback=mentor_find)],
        # show competition
        COMPETITIONS: [MessageHandler(filters=Filters.text, callback=mentor_find)]
    },
    fallbacks=[
        CommandHandler(command='exit', callback=exit_command),
        MessageHandler(filters=Filters.text(["выход"]), callback=exit_command)
    ]
)

if __name__ == "__main__":
    pass
