from bs4 import BeautifulSoup
import requests
import fake_useragent
import csv
from openpyxl import Workbook

data = []


def get_html(url):
    user_agent = fake_useragent.UserAgent(verify_ssl=False)
    user = user_agent.random
    headers = {'User-Agent': str(user)}
    r = requests.get(url, headers=headers)
    return r.text


def parse_first_table(html):
    soup = BeautifulSoup(html, 'lxml')

    list = soup.find('div', id='score-data')

    times = list.find_all('span')
    scores = list.find_all('a')

    for time in times:
        clock = time.text
        data.append([clock])

    for score in scores:
        result = score.text
        data.append([result])

   # write_csv(data)


def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', id='score-data').find_all('a')

    for page in pages:
        link = page.get('href')
        game_link = 'http://m.myscore.ru' + link + '#match-summary'
        prev_game_link = 'https://www.myscore.ru/' + link + '#h2h;overall'


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    team = soup.find('h3').text
    data.append([team])
    bookmaker = soup.find('p', class_='p-set odds-detail').find_all('a')
    for bk in bookmaker:
        data.append([bk.text])


def write_csv(data):
    with open('parsed.csv', 'w', encoding='utf-8', newline='') as file:
        write = csv.writer(file)
        write.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for i in data:
            write.writerow((data['clock'], data['result'], data['team'], data['bk.text']))


def main():
    url = 'http://m.myscore.ru/match/E5cKviws/'
    html = get_html('http://m.myscore.ru/')
    print(get_page_data(get_html(url)))
    jobs = (base_url, headers)
    files_writer(jobs)


if __name__ == '__main__':
    main()
