import requests
import os
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

URL = 'https://adukar.com/by/news/abiturientu/shkolnye-uchebniki-onlajn-virtualnaya-polka'

ua = UserAgent()


def main():
    resp = requests.get(URL, headers={f'User-Agent': ua.random})
    soup = bs(resp.text, 'lxml')
    all_tags_p = soup.find_all('p', dir='ltr')

    if not os.path.exists('school_books'):
        os.mkdir('school_books')

    for num_class in range(5, 12):
        for item in all_tags_p:
            if item.find('a'):
                if item.find('a').get('href').split('.')[-1] == 'pdf' and f'{num_class} клас' in item.find('a').find(
                        'span').text:

                    dir_name = item.find('a').find('span').text.split(str(num_class))[0].strip()
                    link_book = f"https://adukar.com/images/photo/{item.find('a').get('href').split('/')[-1]}"
                    name_book = (item.find('a').find('span').text.split('(')[0]).strip()

                    if not os.path.exists(f'school_books/{dir_name}'):
                        os.mkdir(f'school_books/{dir_name}')

                    if os.path.exists(f'school_books/{dir_name}/{name_book}.pdf'):
                        print(f'Книга {name_book} уже находится в директории')
                        continue
                    else:
                        response = requests.get(link_book, headers={f'User-Agent': ua.random})
                        with open(f'school_books/{dir_name}/{name_book}.pdf', 'wb') as file:
                            file.write(response.content)
                        print(f'...........Скачана {name_book}...........')

    print('Программа завершила свою работу.')


if __name__ == '__main__':
    main()
