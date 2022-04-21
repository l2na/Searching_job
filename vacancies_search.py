import requests
import json


def search_vacancy():
    text = None
    count = None
    while not text or not count:
        text = input('Введи название вакансии: ')
        try:
            count = int(input('Введи число вакансий, которое хочешь увидеть: '))
        except ValueError:
            print('Введи число, а не что-то иное')
    if count > 100:
        pages = count // 100
        vacancies_in_last_page = count - 100
        items = []
        for i in range(1, pages+1):

            resp = requests.get(f'https://api.hh.ru/vacancies?area=1&per_page={100}&text={text}&page{i}')
            try:
                items += json.loads(resp.content)['items']
            except KeyError:
                print('Ничего не нашлось, попробуй изменить запрос и запустить программу заново')
                return search_vacancy()
        resp = requests.get(f'https://api.hh.ru/vacancies?area=1&per_page={vacancies_in_last_page}&text={text}&page={pages+2}')
        try:
            items += json.loads(resp.content)['items']
        except KeyError:
            pass
    else:
        resp = requests.get(f'https://api.hh.ru/vacancies?area=1&per_page={count}&text={text}')
        try:
            items = json.loads(resp.content)['items']
        except KeyError:
            print('Ничего не нашлось, попробуй изменить запрос и запустить программу заново')
            return search_vacancy()

	
    number = 1
    print(f'Ищем среди последних {count} вакансий')
    for item in items:
        name = item['name']
        vacancy_id = item['id']
        link = f'https://kazan.hh.ru/vacancy/{vacancy_id}'
        print(f'{number}. Название - {name}. Ссылка - {link}')
        number += 1
    if len(items) < count:
        print(f'Нашлось только {len(items)} вакансий')


if __name__ == '__main__':
    search_vacancy()
