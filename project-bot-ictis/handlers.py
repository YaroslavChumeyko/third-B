from telegram.ext import MessageHandler, Filters

import topics


def gram_dist(a, b): # Расстояние Дамерау-Левенштайна для анализа грам.ошибок
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_column = range(n+1)
    for i in range(1, m+1):
        previous_column, current_column = current_column, [i]+[0]*n
        for j in range(1, n + 1):
            add, delete, change = previous_column[j] + 1, current_column[j-1] + 1, previous_column[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_column[j] = min(add, delete, change)

    return current_column[n] / n


def text_reply(update, bot):
    text_message = update.message.text
    for greeting in topics.greet_list:
        if gram_dist(greeting, text_message.lower()) <= 0.3:
            return greetings(update, bot)
    return bot.bot.sendMessage(chat_id=update.message.chat_id, text=text_message)


def greetings(update, bot):
    bot.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"Здравствуй, { update.message.from_user.first_name }"
        )


text_handler = MessageHandler(Filters.text, text_reply)
