import requests
import json
import time


# Класс для обработки исключений при работе с API

class GetAPIDataError(Exception):

    def __init__(self):
        self.message = "GetAPIDataError: Ошибка получения данных от API"

    def __str__(self):
        return self.message


# Класс для работы с API HH

class HeadHunterApi:

    def __init__(self, employee_dict: dict):
        self.employee_dict = employee_dict
        self.employee_json_data = []
        self.vacancy_json_data = []

    def get_vacancies_from_hh(self):
        """
        Метод получения данных по вакансиям от HH API
        Считывает максимально возможное количество вакансий
        по указанным работодателям и возвращает json raw список.
        :return: Список raw json со всеми данными по вакансиям
        """
        json_data_list = []
        try:
            for employee in self.employee_dict:
                print(f'Считываются вакансии организации {self.employee_dict[employee]}')
                for pages in range(0, 20):  # Читаем в цикле все страницы данных по вакансиям
                    params = {
                        'host': 'hh.ru',
                        'employer_id': employee,
                        'locale': 'RU',
                        'area': 113,
                        'page': pages,
                        'per_page': 100
                    }
                    recs = requests.get("https://api.hh.ru/vacancies", params)
                    json_record = json.loads(recs.content.decode())  # Приводим полученные данные к формату json
                    json_data_list.extend(json_record['items'])  # Добавляем данные каждой страницы в общий список
                    if (json_record['pages'] - pages) <= 1:  # Если страниц меньше 20, дочитываем и прерываем цикл
                        break
                    print(f'Загрузка страницы - {pages}')
                    time.sleep(0.20)  # Задержка на запрос, чтобы не загружать сервер HH
        except GetAPIDataError:
            print(GetAPIDataError())
        self.vacancy_json_data = json_data_list

    def get_vacancies_items(self) -> list:
        """
        Метод для обработки вакансий.
        Выбирает конкретные поля и объединяет в список кортежей.
        В случае отсутствия данных - формирует их.
        :return: Список кортежей с выбранными данными по вакансиям
        """
        vacation_item_list = []

        # Форматируем данные полученные от API
        for items in self.vacancy_json_data:
            vacancy_data_1 = (items['id'], items['name'], items['employer']['id'])

            # Формируем поля З/П если не указана
            if items['salary'] is not None:
                if items['salary']['from'] is not None:
                    salary_from = items['salary']['from']
                else:
                    salary_from = None
                if items['salary']['to'] is not None:
                    salary_to = items['salary']['to']
                else:
                    salary_to = None
            else:
                salary_from = None
                salary_to = None

            # формируем второй кортеж с данными, объединяем кортежи и добавляем в список
            vacancy_data_2 = (salary_from, salary_to, items['alternate_url'], items['snippet']['requirement'])
            vacancy_data = vacancy_data_1 + vacancy_data_2
            vacation_item_list.append(vacancy_data)
        return vacation_item_list

    def get_employee_data(self):
        """
        Метод получения данных по работодателям от HH API
        Считывает данные по указанным работодателям и возвращает json raw список.
        :return: Список raw json со всеми данными по работодателям
        """
        json_data_list = []
        try:
            # Перебираем список работодателей по ключам
            for employee_id in self.employee_dict.keys():
                print(f'Получение данных о работодателе {self.employee_dict[employee_id]}')
                recs = requests.get('https://api.hh.ru/employers/' + str(employee_id))      # Опрос API
                json_record = json.loads(recs.content.decode())  # Приводим полученные данные к формату json
                json_data_list.append(json_record)
        except GetAPIDataError:
            print(GetAPIDataError())

        self.employee_json_data = json_data_list

    def get_employee_items(self) -> list:
        """
        Метод для обработки данных работодателей.
        Выбирает конкретные поля и объединяет в список кортежей.
        В случае отсутствия данных - формирует их.
        :return: Список кортежей с выбранными данными работодателей
        """
        employee_item_list = []

        # Форматируем данные полученные от API
        for items in self.employee_json_data:
            industries_record = ''
            employee_tuple_1 = (items['id'], items['name'], items['area']['name'],
                                items['site_url'])

            # Обрабатываем данные по специализации организации, если их несколько - объединяем в строку
            if items['industries'] != []:
                for recs in items['industries']:
                    industries_record += recs['name'] + '. '
                industries = industries_record
            else:
                industries = 'Не указано.'

            employee_tuple_2 = (items['alternate_url'], industries)         # формируем второй кортеж с данными
            employee_item_list.append(employee_tuple_1 + employee_tuple_2)  # Объединяем кортежи, добавляем в список
        return employee_item_list
