import json
import requests
from bs4 import BeautifulSoup
from bs4 import Tag, ResultSet


HOST = 'https://www.litmir.me/bs/?rs=5%7C1%7C0'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
PHOTO = 'https://www.litmir.me'

def get_db(db):
    with open(f'{db}.json', 'r') as file:
        return json.load(file)


def write_db(data, db):
    with open(f'{db}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    

def get_html(url: str, headers: dict='', params: str=''):
    """ Функция для получения html кода """
    html = requests.get(
        url,
        headers=headers,
        params=params,
        verify=False
    )
    return html.text


def get_card_from_html(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('table', class_='island')
    return cards

def get_photo(cards):
    result = []
    for card in cards:
        photo = PHOTO + card.find('td', class_='lt22').find('a').find('img').get('data-src')
        result.append(photo)
    return result



def get_author(cards):
    result = []
    for card in cards:
        author = card.find('span', class_='desc2').text.strip()
        result.append(author)
    return result

def get_page(cards):
    result = []
    for card in cards:
        pages = card.find_all('span', class_='desc2')
        for page in pages:
            num = page.text.strip()
            if len(num) < 4:
                result.append(num)
    return result

def get_title(cards):
    result = []
    for card in cards:
        title = card.find('div', class_='book_name').text 
        result.append(title)
    return result

def get_genre(cards):
    result = []
    for card in cards:
        genres = card.find('span', itemprop='genre').text.split(',')[0]
        result.append(genres)
    return result



def parse_data_from_cards(cards) -> list:
    result = []
    db = get_db('books')
    title = get_title(cards)
    photo = get_photo(cards)
    author = get_author(cards)
    page = get_page(cards)
    genre = get_genre(cards)
    len_num = len(title)
    for num in range(len_num):
        obj = {
            'title': title[num],
            'image': photo[num],
            'author': author[num], 
            'page': page[num],
            'genre': genre[num]
        }
        db.append(obj)
    write_db(db, 'books')



# if __name__ == '__main__':
#     html = get_html(HOST) 
#     cards = get_card_from_html(html)
#     c = parse_data_from_cards(cards)

