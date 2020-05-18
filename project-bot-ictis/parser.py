#Очень черновая версия!!!
#!/usr/bin/env python3
import csv
import json
import requests
from bs4 import BeautifulSoup
BASE_URL = 'https://proictis.sfedu.ru/api/mentors'


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
    all_mentors = []
    for i in range(len(json_list)):
        name = json_list[i]['name']
        patronymic = json_list[i]['patronymic']
        surname = json_list[i]['surname']
        full_name = ' '.join([surname, name, patronymic])

        email = json_list[i]['email']
        phone = json_list[i]['phone']
        post = json_list[i]['post']
        direction = json_list[i]['directions']

        all_mentors.append([])
        all_mentors[i].append(full_name)
        all_mentors[i].append(email)
        all_mentors[i].append(phone)
        all_mentors[i].append(post)
        all_mentors[i].append(direction)
    return all_mentors


def save(projects, path):
    with open(path, 'w', encoding='utf-8', newline="", errors="replace") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SNP', 'email', 'phone', 'post', 'direction'])
        #writer.writerows(
        #    (project['fio'], ', '.join(project['email']), project['position'],
        #    project['direction']) for project in projects)
        writer.writerows(projects)



def main():
    projects = json.loads(get_html(BASE_URL))
    projects = parse_mentors(projects)
    for mentor in projects:
        print(mentor)


    #projects = parse(projects)
    #(projects)

    print('Сохранение...')
    save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
