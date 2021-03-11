import csv
from bs4 import BeautifulSoup as bs
import requests

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page=0'


def hh_parse(base_url, headers):
    global requests

    jobs = []
    urls = []
    urls.append(base_url)

    session = requests.Session()
    requests = session.get(base_url, headers=headers)

    if requests.status_code == 200:
        soup = bs(requests.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        requests = session.get(url, headers=headers)
        soup = bs(requests.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.strip()
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = text1 + ' ' + text2
            jobs.append({
                'title': title,
                'href': href,
                'company': company,
                'content': content
            })
        write_csv(jobs)
    else:
        print('ERROR or DONE. Status_code = ' + '' + str(requests.status_code))
    return jobs


def write_csv(jobs):
    with open('parsed_jobs.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            writer.writerow((job['title'], job['href'], job['company'], job['content']))


jobs = hh_parse(base_url, headers)
write_csv(jobs)
