# Очень черновая версия!!!
#!/usr/bin/env python3
import csv
import json
import requests
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


def parse_mentors(json_list):
    all_mentors = {
        'name': [],
        'email': [],
        'phone': [],
        'post': [],
        'directions': []
    }
    for i in range(len(json_list)):
        all_mentors['name'].append(
            ' '.join([json_list[i]['surname'], json_list[i]['name'], json_list[i]['patronymic']])
        )
        all_mentors['email'].append(json_list[i]['email'])
        all_mentors['phone'].append(json_list[i]['phone'])
        all_mentors['post'].append(json_list[i]['post'])
        all_mentors['directions'].append(json_list[i]['directions'])
    return all_mentors


def mentors_list():
    mentors = json.loads(get_html(BASE_URL + url_path['mentors']))
    mentors = parse_mentors(mentors)
    return mentors


def mentors_names():
    mentors = mentors_list()
    bot_message = '-'+'\n-'.join(mentors['name'])
    return bot_message


def one_mentor(name):
    mentors = mentors_list()
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
    projects = json.loads(get_html(BASE_URL + url_path['mentors']))
    projects = parse_mentors(projects)
    for key, value in projects.items():
        print(key, value)
    a = one_mentor("Кучеров")
    print(a)


    # projects = parse(projects)
    # (projects)

    # print('Сохранение...')
    # save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
