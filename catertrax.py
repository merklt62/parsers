import requests
import csv
from bs4 import BeautifulSoup


def get_html(url):
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
    r = requests.get(url, headers=user_agent)
    return r.text


def write_csv(data):
    with open('testimonials.csv', 'a') as f:
        order = ['author', 'since', 'email', 'tel']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_articles(html):
    soup = BeautifulSoup(html, 'lxml')
    ts = soup.find('div', class_='testimonial-container').find_all('article')
    return ts


def get_page_data(ts):
    for t in ts:
        try:
            since = t.find('p', class_='traxer-since').text.strip()
        except:
            since = ''
        try:
            author = t.find('p', class_='testimonial-author').text.strip()
        except:
            author = ''
        try:
            email = t.find('ul', class_='testimonial-meta').find('li', class_='email').text.strip()
        except:
            email = ''
        try:
            tel = t.find('ul', class_='testimonial-meta').find('li', class_='tel').text.strip()
        except:
            tel = ''
        data = {'author': author, 'since': since, 'email': email, 'tel': tel}
        write_csv(data)


def main():
#    1. Получение контейнера с отзывами и списка отзывов
#    2. Если список есть, то парсим отзыв
#    3. усли список пустой - цикл прерывается
    while True:
        page = 1
        url = 'https://catertrax.com/why-catertrax/traxers/page/{}/'.format(str(page))

        articles = get_articles(get_html(url))

        if articles:
            get_page_data(articles)
            page = page + 1
        else:
            break


if __name__ == '__main__':
    main()
