# Очень черновая версия!!!
#!/usr/bin/env python3
import csv
import json
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
    'achievements': '/api/achievements'
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


def parse_info(json_list, nes_info):
    for i in range(len(json_list)):
        for key in nes_info.keys():
            if key == 'name':
                snp = ' '.join([json_list[i]['surname'], json_list[i]['name'], json_list[i]['patronymic']])
                if snp not in nes_info[key]:
                    nes_info[key].append(snp)
            else:
                if json_list[i][key] not in nes_info[key]:
                    nes_info[key].append(json_list[i][key])
    return nes_info


def mentors_list(section, nes_info):
    mentors = parse_info(json.loads(get_html(BASE_URL + url_path[section])), nes_info)
    return mentors


def find_info(section, nes_info, out_info):
    info = mentors_list(section, nes_info)
    bot_message = '-'+'\n-'.join(info[out_info][::-1])
    return bot_message


def one_mentor(name, section, nes_info):
    mentors = mentors_list(section, nes_info)
    for i in range(len(mentors['name'])):
        if name in mentors['name'][i]:
            return "\n".join([j[i] for j in mentors.values()])


def save(projects, path):
    with open(path, 'w', encoding='utf-8', newline="", errors="replace") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SNP', 'email', 'phone', 'post', 'direction'])
        # writer.writerows(
        #    (project['fio'], ', '.join(project['email']), project['position'],
        #    project['direction']) for project in projects)
        writer.writerows(projects)


def main():
    projects = mentors_list(url_path['mentors'], bot_topics.mentors_info)
    print(projects)

    print(one_mentor('Кучеров', url_path['mentors'], bot_topics.mentors_info))

    # projects = parse(projects)
    # (projects)

    # print('Сохранение...')
    # save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
