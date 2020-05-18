from pymorphy2 import MorphAnalyzer

from topics import topics


def gram_dist(s1, s2): # Расстояние Дамерау-Левенштайна для анализа грам. ошибок
    d = {}
    l1 = len(s1)
    l2 = len(s2)
    for i in range(-1, l1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, l2 + 1):
        d[(-1, j)] = j + 1

    for i in range(l1):
        for j in range(l2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,
                d[(i, j - 1)] + 1,
                d[(i - 1, j - 1)] + cost,
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)

    return d[l1 - 1, l2 - 1] / max(l1, l2)


def text_filter(update, bot):
    text_message = update.message.text.split()
    morph = MorphAnalyzer()
    for i in range(len(text_message)):
        text_form = morph.parse(text_message[i])
        text_message[i] = text_form[0].normal_form

    for topic_words in topics.values():
        for top_word in topic_words:
            for i in range(len(text_message)):
                if gram_dist(text_message[i], top_word) <= 0.4:
                    text_message[i] = top_word

    update.message.text = ' '.join(text_message)
    bot.bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text
    )


if __name__ == "__main__":
    pass
