//Очень черновая версия!!!
#!/usr/bin/env python3
import csv
import urllib.request
from bs4 import BeautifulSoup
BASE_URL = 'https://proictis.sfedu.ru/mentors'
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()
def get_page_count(html):
    soup = BeautifulSoup(html)
    paggination = soup.find('div', class_='pages_list text_box')
    return int(paggination.find_all('a')[-2].text)
def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', class_='row cc_cursor')
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
def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('ФИО', 'Почта', 'Должность', 'Направление'))
        writer.writerows(
            (project['fio'], ', '.join(project['email']), project['position'], project['direction']) for project in projects
        )
def main():
    projects = []
    print('Сохранение...')
    save(projects, 'projects.csv')
if __name__ == '__main__':
    main()
