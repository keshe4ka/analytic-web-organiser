import requests
from bs4 import BeautifulSoup


def get_info_from_post(url, bookmarks_group_id):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # TODO
    # берем title

    # берем титульную картинку

    # берем основной текст

    element_dict = {
        'title': 'title',
        'img_src': 'title',
        'tags': 'tags',
        'source': url,
        'bookmarks_group_id': bookmarks_group_id
    }
    return element_dict
