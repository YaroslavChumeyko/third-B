# Очень черновая версия!!!
#!/usr/bin/env python3
import csv
import requests
import bot_topics
from bs4 import BeautifulSoup


BASE_URL = 'https://proictis.sfedu.ru'
url_path = {
    'contacts': '/about',
    'mentors': '/api/mentors',
    'projects': '/api/projects',
    'news': '/api/news',
    'competitions': '/api/competitions',
    'achievements': '/api/achievements',
    'login': 'api/login',
    'requests': 'api/me/requests',
    'archive': 'api/chat/archive',
    'chats': 'api/chats'
}


def get_html(url):
    response = requests.get(url)
    return response.text


def get_page_count(html):
    soup = BeautifulSoup(html)
    paggination = soup.find('div', class_='pages_list text_box')
    return int(paggination.find_all('a')[-2].text)


def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', class_='row cc_cursor')
    print(table)
    rows = table.find_all('div', class_='col-lg-6 mentor-wrapper ng-star-inserted')
    projects = []
    for row in rows:
        cols = row.find_all('mat-card-title', 'mat-card-subtitle', )
        projects.append({
            'fio': cols[0].a.text,
            'email': [category.text for category in cols[0].find_all('noindex')],
            'position': cols[1].text.strip().split()[0],
            'direction': cols[2].text.split()[0]
        })
    return projects


# Processing JSON object function block
# Global overview functions
def json_parse_info(json_list: dict, nes_info: dict):
    for i in range(len(json_list)):
        for key in json_list[i].keys():
            if key == 'name':
                try:
                    json_list[i][key] = ' '.join([
                        json_list[i]['surname'],
                        json_list[i]['name'],
                        json_list[i]['patronymic'],
                    ])
                except KeyError:
                    pass
        for key in reversed(sorted(json_list[i].keys())):
            if key not in nes_info.keys():
                del json_list[i][key]
    return json_list


def json_info_listing(section: str, nes_info: dict):
    json_list = requests.get(BASE_URL + url_path[section]).json()
    info = json_parse_info(json_list, nes_info)
    return info


def json_find_info(section: str, nes_info: dict, out_info: list):
    info = json_info_listing(section, nes_info)
    if section == 'mentors':
        bot_message = '-'+'\n-'.join([i[out_info[0]] for i in info])+'\n\n'
    else:
        bot_message = ""
        n = len(info) - 1
        for i in range(n, n-4, -1):
            bot_message += ("<b>-%s</b>\n" % str(info[i][out_info[0]]))
            try:
                bot_message += ("\t%s\n\n" % str(info[i][out_info[1]]))
            except IndexError:
                bot_message += ("\t\n\n")
    return bot_message + 'Напишите "выход", чтобы прервать текущее действие'


# Single site-object inspection
def json_one_subject(find_info: str, out_info: list, key: str, section: str, nes_info: dict):
    json_list = json_info_listing(section, nes_info)
    for subject in json_list:
        if find_info in subject[key].lower().replace("ё", "е"):
            bot_message = "<b>" + str(subject[key]) + "</b>\n\n"
            for i in range(1, len(out_info)):
                bot_message += nes_info[out_info[i]] + subject[out_info[i]] + "\n"
            return bot_message.replace(3*'\n', 2*'\n')


def save(projects, path):
    with open(path, 'w', encoding='utf-8', newline="", errors="replace") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SNP', 'email', 'phone', 'post', 'direction'])
        # writer.writerows(
        #    (project['fio'], ', '.join(project['email']), project['position'],
        #    project['direction']) for project in projects)
        writer.writerows(projects)


# Test field :)
def main():
    projects = json_find_info(
        'news',
        bot_topics.news_info,
        ['title', 'shortDescription']
    )
    print(projects)

    print(json_one_subject('Кучеров', 'mentors', bot_topics.mentors_info))

    # projects = parse(projects)
    # (projects)

    # print('Сохранение...')
    # save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
