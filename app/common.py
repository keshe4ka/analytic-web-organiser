import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
import nltk

categories = ['.net', 'big data', 'c#', 'c++', 'devops', 'diy или сделай сам', 'it-инфраструктура', 'it-компании',
              'java',
              'javascript', 'open source', 'php', 'python', 'алгоритмы', 'анализ и проектирование систем',
              'биотехнологии',
              'высокая производительность', 'гаджеты', 'дизайн', 'законодательство в it', 'звук', 'здоровье',
              'игры и игровые консоли', 'интерфейсы', 'информационная безопасность', 'искусственный интеллект',
              'исследования и прогнозы в it', 'история it', 'карьера в it-индустрии', 'компьютерное железо',
              'конференции',
              'космонавтика', 'математика', 'машинное обучение', 'настройка linux', 'научно-популярное',
              'программирование',
              'разработка веб-сайтов', 'разработка игр', 'разработка мобильных приложений', 'разработка под android',
              'разработка под ios', 'робототехника', 'сетевые технологии', 'системное администрирование', 'смартфоны',
              'софт',
              'cоциальные сети и сообщества', 'тестирование it-систем', 'транспорт', 'управление персоналом',
              'управление продуктом', 'управление проектами', 'учебный процесс в it', 'физика', 'финансы в it',
              'энергия и элементы питания']


def get_info_from_post(url, bookmarks_group_id, model):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # TODO
    # берем title
    title = ''
    # берем титульную картинку
    img_save = ''
    img_src = ''
    # берем основной текст
    text = r'iphone'

    # распознаем теги
    df = pd.DataFrame({'text': [text]})
    df['text'][0] = text_preprocess(df['text'][0])
    data = df['text']
    predict = model.predict(data)
    predict = predict[0].tolist()
    tags = []
    for i in range(0, len(predict)):
        if predict[i] == 1:
            tags.append(categories[i])

    element_dict = {
        'title': title,
        'img_src': img_src,
        'tags': tags,
        'source': url,
        'bookmarks_group_id': bookmarks_group_id
    }
    return element_dict


def text_preprocess(sentence):
    def keep_alpha(sentence):
        alpha_sentence = re.sub('[^a-z A-Z а-я А-Я]+', ' ', sentence)
        return alpha_sentence

    def remove_tags(sentence):
        html_tag = '<.*?>'
        cleaned_sentence = re.sub(html_tag, ' ', sentence)
        return cleaned_sentence

    def remove_punctuation(sentence):
        cleaned_sentence = re.sub(r'[?|!|\'|"|#]', '', sentence)
        cleaned_sentence = re.sub(r'[,|.|;|:|(|)|{|}|\|/|<|>]|-', ' ', cleaned_sentence)
        cleaned_sentence = cleaned_sentence.replace("\n", " ")
        return cleaned_sentence

    def remove_stop_words(sentence):
        stop_words = set(stopwords.words('russian'))
        stop_words.update(
            ['хабр', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять', 'это',
             'который', 'например', 'все', 'всё', 'весь', 'gt', 'lt', 'br', 'использовать', 'также', 'каждый', 'свой',
             'еще', 'ещё', 'мочь'])
        no_stop_words = [word for word in sentence.split() if word not in stop_words]
        no_step_sentence = ' '.join(no_stop_words)
        return no_step_sentence

    def lower_case(sentence):
        lower_case_sentence = sentence.lower()
        return lower_case_sentence

    def lemmatize_words(sentence):
        morph = pymorphy2.MorphAnalyzer()
        lemmatized_words = [morph.parse(word)[0].normal_form for word in sentence.split()]
        lemmatized_sentence = ' '.join(lemmatized_words)
        return lemmatized_sentence

    pre_processed_sentence = remove_tags(sentence)
    pre_processed_sentence = remove_punctuation(pre_processed_sentence)
    pre_processed_sentence = keep_alpha(pre_processed_sentence)
    pre_processed_sentence = lower_case(pre_processed_sentence)
    pre_processed_sentence = lemmatize_words(pre_processed_sentence)
    pre_processed_sentence = remove_stop_words(pre_processed_sentence)
    return pre_processed_sentence

# import joblib
# import sklearn
# import nltk
# #
# # nltk.download('stopwords')
# #
# # for test only
# model = joblib.load('/Users/artem_anaschenko/PycharmProjects/analytic_web_organiser/model.joblib')
# print('uraaaa')
# el = get_info_from_post('aaa', 1, model)
# print(el)
