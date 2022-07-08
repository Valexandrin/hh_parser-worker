import json
import time
from worker.config import config

import httpx

hh_api = config.source.url
endpoint = f'{config.endpoint.url}/vacancies'


def get_vacancies(page=1):
    params = {
            'text': 'NAME:Python (разработчик OR developer OR программист) NOT (full-stack OR fullstack OR middle OR senior), удаленная работа',
            'page': page, # Индекс страницы поиска на HH
            'per_page': 100 # Кол-во вакансий на 1 странице
        }

    response = httpx.get(url=hh_api, params=params)
    vacancies = data_processing(response)

    return vacancies


def get_description(vacancy_id):
    response = httpx.get(url='{hh_api}/{id}'.format(hh_api=hh_api, id = vacancy_id))

    vacancy = data_processing(response)

    return vacancy['description']


def data_processing(input_data):
    data = input_data.content.decode()

    return json.loads(data)


def save_vacancy(vacancy):
    params = {
            'uid': vacancy['id'],
            'area': vacancy['area']['name'],
            'description': vacancy['description'],
            'employer': vacancy['employer']['name'],
            'name': vacancy['name'],
            'published_at': vacancy['published_at'],
            'requirement': vacancy['snippet']['requirement'],
            'responsibility': vacancy['snippet']['responsibility'],
            'schedule': vacancy['schedule']['name'],
            'status': 'new',
            'url': vacancy['alternate_url'],
        }

    if vacancy['salary']:
        if vacancy['salary']['from']:
            params['salary_from'] = vacancy['salary']['from']
        if vacancy['salary']['to']:
            params['salary_to'] = vacancy['salary']['to']

    httpx.post('{endpoint}/'.format(endpoint=endpoint), json=params)


def db_update():
    id_list = []
    pages = get_vacancies()['pages']
    for page in range(pages):
        vacancies = get_vacancies(page)['items']
        for vacancy in vacancies:
            exist_vacancy = httpx.get('{endpoint}/{vacancy_id}'.format(
                endpoint=endpoint,
                vacancy_id=vacancy['id'],
            ))

            if exist_vacancy.status_code != 200:
                vacancy['description'] = get_description(vacancy['id'])

                save_vacancy(vacancy)

            id_list.append(int(vacancy['id']))

    db_clean(id_list)


def db_clean(actual_ids: list):
    db_vacancies = httpx.get('{endpoint}/'.format(endpoint=endpoint)).json()

    for db_vacancy in db_vacancies:
        if db_vacancy['uid'] not in actual_ids:
            httpx.delete('{endpoint}/{uid}'.format(
                endpoint=endpoint,
                uid=db_vacancy['uid'],
            ))


def run_parser(delay):
    while True:
        db_update()
        time.sleep(delay)


if __name__ == '__main__':
    run_parser()
