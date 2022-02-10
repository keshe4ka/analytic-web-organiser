import re
import ratelim
import requests
from requests_html import HTMLSession
from requests import exceptions
from bs4 import BeautifulSoup
from time import sleep

# habr_url = 'https://habr.com/ru/post/'
habr_url = 'https://habr.com/ru/post/596491/'
count_of_posts = 100000


@ratelim.patient(1, 1)
def get_data_from_post():
    # url = habr_url + str(post_id)
    url = habr_url
    try:
        response = requests.get(url)
        response.raise_for_status()
        title, text, habs, rating, bookmarks, comments, user, date = get_elements(response)
        # print(f'{title} \n {text} \n  {habs}')
        print(date)
    except requests.exceptions.HTTPError as ex:
        pass


def get_elements(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    # Заголовок
    title = soup.find('meta', property='og:title')
    title = str(title).split('="')[1].split('" ')[0]

    # Текст
    text = str(soup.find('div', id="post-content-body"))
    text = re.sub(r'\<[^>]*\>', '', text)
    text = re.sub('\n', ' ', text)

    # Хабы
    habs = str(soup.findAll('a', class_="tm-hubs-list__link"))
    habs = re.sub(r'\<[^>]*\>', '', habs)
    habs = re.sub('\s+', ' ', habs)

    # Рейтинг
    rating = str(soup.find('span',
                           class_='tm-votes-meter__value tm-votes-meter__value_positive tm-votes-meter__value_appearance-article tm-votes-meter__value_rating'))
    rating = int(re.sub(r'\<[^>]*\>', '', rating))

    # Кол-во сохранений
    bookmarks = str(soup.find('span', class_='bookmarks-button__counter'))
    bookmarks = int(re.sub(r'\<[^>]*\>', '', bookmarks))

    # Кол-во комментариев
    comments = str(soup.find('span',
                             class_='tm-article-comments-counter-link__value tm-article-comments-counter-link__value_contrasted'))
    comments = re.sub(r'\<[^>]*\>', '', comments)
    comments = int(re.sub(r'\D', '', comments))

    # Автор
    user = str(soup.find('span', class_='tm-user-info__user'))
    user = re.sub(r'\<[^>]*\>', '', user)
    user = re.sub(r'\s', '', user)

    # Дата публикации
    date = str(soup.find('span', class_='tm-article-snippet__datetime-published'))
    date = re.sub(r'\<[^>]*\>', '', date)

    return title, text, habs, rating, bookmarks, comments, user, date


if __name__ == '__main__':
    get_data_from_post()
