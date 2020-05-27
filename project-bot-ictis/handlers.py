from telegram.ext import MessageHandler
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters

# from bot_filter import text_filter
import bot_topics
import site_logic


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
# Bot displays site information overview
def do_display(update, bot, section, nes_info, out_info):
    bot_message = site_logic.json_find_info(
        section=section,
        nes_info=nes_info,
        out_info=out_info
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_message
    )


def do_mentors(update, bot):
    do_display(
        update=update,
        bot=bot,
        section='mentors',
        nes_info=bot_topics.mentors_info,
        out_info=['name']
    )
    return MENTORS


def do_news(update, bot):
    do_display(
        update=update,
        bot=bot,
        section='news',
        nes_info=bot_topics.news_info,
        out_info=['title', 'shortDescription']
    )
    return NEWS


def do_achievements(update, bot):
    do_display(
        update=update,
        bot=bot,
        section='achievements',
        nes_info=bot_topics.achievements_info,
        out_info=['title', 'shortDescription']
    )
    return ACHIEVEMENTS


def do_competitions(update, bot):
    do_display(
        update=update,
        bot=bot,
        section='competitions',
        nes_info=bot_topics.competitions_info,
        out_info=['title', 'deadline']
    )
    return COMPETITIONS


# Detailed information from site
def find_display(update, bot, out_info, key, section, nes_info):
    user_message = update.message.text
    if user_message == 'выход':
        return exit_command(update, bot)
    bot_answer = site_logic.json_one_subject(
        find_info=user_message,
        out_info=out_info,
        key=key,
        section=section,
        nes_info=nes_info
    )
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=bot_answer
    )
    return "continue"


def find_mentor(update, bot):
    bot_answer = find_display(
        update=update,
        bot=bot,
        out_info=list(bot_topics.mentors_info.keys()),
        key='name',
        section='mentors',
        nes_info=bot_topics.mentors_info
    )
    if bot_answer == "continue":
        return MENTORS
    else:
        return bot_answer


def find_news(update, bot):
    bot_answer = find_display(
        update=update,
        bot=bot,
        out_info=['title', 'description'],
        key='title',
        section='news',
        nes_info=bot_topics.news_info
    )
    if bot_answer == "continue":
        return NEWS
    else:
        return bot_answer


def find_achievement(update, bot):
    bot_answer = find_display(
        update=update,
        bot=bot,
        out_info=['title', 'description'],
        key='title',
        section='achievements',
        nes_info=bot_topics.achievements_info
    )
    if bot_answer == "continue":
        return ACHIEVEMENTS
    else:
        return bot_answer


def find_competition(update, bot):
    bot_answer = find_display(
        update=update,
        bot=bot,
        out_info=['title', 'description'],
        key='title',
        section='competitions',
        nes_info=bot_topics.competitions_info
    )
    if bot_answer == "continue":
        return COMPETITIONS
    else:
        return bot_answer


# filter_handler = MessageHandler(filters=Filters.text, callback=text_filter)
# project_handler = MessageHandler(filters=Filters.regex('хочу записаться'), callback=project_sign)
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
        MENTORS: [MessageHandler(filters=Filters.text, callback=find_mentor)],
        # show news
        NEWS: [MessageHandler(filters=Filters.text, callback=find_news)],
        # show achievement
        ACHIEVEMENTS: [MessageHandler(filters=Filters.text, callback=find_achievement)],
        # show competition
        COMPETITIONS: [MessageHandler(filters=Filters.text, callback=find_competition)]
    },
    fallbacks=[
        CommandHandler(command='exit', callback=exit_command),
        MessageHandler(filters=Filters.text(["выход"]), callback=exit_command)
    ]
)

if __name__ == "__main__":
    pass
