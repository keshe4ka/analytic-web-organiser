import re
import ratelim
import requests
from bs4 import BeautifulSoup
import pandas as pd

habr_url = 'https://habr.com/ru/post/'
count_of_posts = 100000
df = pd.DataFrame(columns=['url', 'title', 'text', 'habs', 'tags',
                           'rating', 'bookmarks', 'comments',
                           'user', 'date'])


# \=[-@ratelim.patient(3, 1)
def get_data_from_post(post_id):
    url = habr_url + str(post_id)

    try:
        response = requests.get(url)
        response.raise_for_status()
        title, text, habs, tags, rating, bookmarks, comments, user, date = get_elements(response)
        data_from_page = {'url': url, 'title': title, 'text': text, 'habs': habs, 'tags': tags, 'rating': rating,
                          'bookmarks': bookmarks, 'comments': comments, 'user': user, 'date': date}
        return data_from_page
    except:
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
    habs = habs.split(',')
    for i in range(len(habs)):
        habs[i] = re.sub(r'\[|\]', '', habs[i])
        habs[i] = habs[i].strip()
        habs[i] = habs[i].lower()

    # Теги
    try:
        tags = str(soup.findAll('a', class_="tm-tags-list__link"))
        tags = re.sub(r'\<[^>]*\>', '', tags)
        tags = re.sub('\s+', ' ', tags)
        tags = tags.split(',')
        for i in range(len(tags)):
            tags[i] = re.sub(r'\[|\]', '', tags[i])
            tags[i] = tags[i].strip()
            tags[i] = tags[i].lower()
    except Exception as ex:
        print(ex)
        tags = 'None'

    # Рейтинг
    try:
        rating = str(soup.find('span',
                               class_='tm-votes-meter__value tm-votes-meter__value_positive tm-votes-meter__value_appearance-article tm-votes-meter__value_rating'))
        rating = int(re.sub(r'\<[^>]*\>', '', rating))
    except Exception as ex:
        print(ex)
        rating = 0

    # Кол-во сохранений
    try:
        bookmarks = str(soup.find('span', class_='bookmarks-button__counter'))
        bookmarks = int(re.sub(r'\<[^>]*\>', '', bookmarks))
    except Exception as ex:
        print(ex)
        bookmarks = 0

    # Кол-во комментариев
    try:
        comments = str(soup.find('span',
                                 class_='tm-article-comments-counter-link__value tm-article-comments-counter-link__value_contrasted'))
        comments = re.sub(r'\<[^>]*\>', '', comments)
        comments = int(re.sub(r'\D', '', comments))
    except Exception as ex:
        print(ex)
        comments = 0

    # Автор
    try:
        user = str(soup.find('span', class_='tm-user-info__user'))
        user = re.sub(r'\<[^>]*\>', '', user)
        user = re.sub(r'\s', '', user)
    except Exception as ex:
        print(ex)
        user = 'Null'

    # Дата публикации
    try:
        date = str(soup.find('span', class_='tm-article-snippet__datetime-published'))
        date = re.sub(r'\<[^>]*\>', '', date)
    except Exception as ex:
        print(ex)
        date = 'Null'

    return title, text, habs, tags, rating, bookmarks, comments, user, date


if __name__ == '__main__':
    for i in range(20000, 80000):
        try:
            data = get_data_from_post(i)
            if data is None:
                pass
            else:
                data = pd.DataFrame([data])
                print(data.head())
                df = pd.concat([df, data], ignore_index=True)
        except:
            pass
        if i % 1000 == 0:
            print(i, end=' ')
    print(df.head())
    df.to_csv('/home/keshe4ka/Документы/habr20000_80000.csv', line_terminator="\r\n", index=False)
