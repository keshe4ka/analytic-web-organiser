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
        title, text, habs = get_elements(response)
        # print(f'{title} \n {text} \n  {habs}')
        print(habs)
    except requests.exceptions.HTTPError as ex:
        pass


def get_elements(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('meta', property='og:title')
    title = str(title).split('="')[1].split('" ')[0]

    text = str(soup.find('div', id="post-content-body"))
    text = re.sub(r'\<[^>]*\>', '', text)
    text = re.sub('\n', ' ', text)

    habs = str(soup.findAll('a', class_="tm-hubs-list__link"))
    habs = re.sub(r'\<[^>]*\>', '', habs)
    habs = re.sub('\s+', ' ', habs)

    statistic = soup.find('ul', attrs={'class': 'post-stats post-stats_post js-user_'})

    return title, text, habs


if __name__ == '__main__':
    get_data_from_post()
