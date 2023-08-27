import psycopg2
import psycopg2.errors


# Класс работы с базой данных

class DBManager:

    def __init__(self):
        self.init_error = False
        try:
            self.__connection = psycopg2.connect(host='localhost', database='headhunter',
                                                 user='postgres', password='TranQuillita')
        except psycopg2.OperationalError:
            print("\nОТСУТСТВУЕТ СВЯЗЬ С БАЗОЙ ДАННЫХ, ПРОВЕРЬТЕ НАЛИЧИЕ БД ИЛИ СЕТЕВОЕ СОЕДИНЕНИЕ")
            self.init_error = True

    def insert_data_into_db(self, table_data: list, hh_data: list):
        """
        Метод заполнения таблиц данными
        :param table_data: формат записи для таблицы
        :param hh_data:
        :return:
        """
        try:
            with self.__connection as conn:
                # Открываем курсор для работы с БД, с таблицей customers
                with conn.cursor() as cur:
                    # Выполняем SQL-запрос в цикле с подстановкой данных
                    for custom_record in hh_data:
                        cur.execute(f"INSERT INTO {table_data[0]} VALUES {table_data[1]}", custom_record)
                    conn.commit()  # Запись данных в таблицу customers
                # Закрываем курсор
                cur.close()
        except psycopg2.errors.UniqueViolation:
            print("\nДАННЫЕ УЖЕ В ТАБЛИЦАХ, ПЕРЕЙДИТЕ К РАБОТЕ С ДАННЫМИ!!!")

    def get_companies_and_vacancies_count(self) -> str:
        """
        Получает из DB список всех компаний и количество вакансий у каждой компании.
        :return: Отформатированная для вывода строка с данными -> str
        """
        query_result = ''
        with self.__connection as conn:
            # Открываем курсор для работы с БД, с таблицей customers
            with conn.cursor() as cur:
                # Выполняем SQL-запрос
                cur.execute(
                    f'SELECT DISTINCT company_name, COUNT(*) FROM company '
                    f'LEFT JOIN vacancy ON vacancy.company_id=company.company_id GROUP BY company_name')
                # Получаем ответ и копируем его в переменную
                query_data = cur.fetchall()
            # Закрываем курсор
            cur.close()
        # Из полученных данных формируем результат в строковом формате с построчным переносом
        for items in query_data:
            query_result += f'{items[0]}, {items[1]}\n'
        return f'{query_result} \nКоличество записей {len(query_data)}'

    def get_all_vacancies(self) -> str:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return: Отформатированная для вывода строка с данными -> str
        """
        query_result = ''
        with self.__connection as conn:
            # Открываем курсор для работы с БД, с таблицей customers
            with conn.cursor() as cur:
                # Выполняем SQL-запрос
                cur.execute(
                    f'SELECT company_name, vacancy_name, salary_from, salary_to, vacancy_url FROM company '
                    f'INNER JOIN vacancy ON vacancy.company_id=company.company_id')
                # Получаем ответ и копируем его в переменную
                query_data = cur.fetchall()
            # Закрываем курсор
            cur.close()
        # Из полученных данных формируем результат в строковом формате с построчным переносом
        for items in query_data:
            query_result += f'{items[0]}, {items[1]}, {items[2]}, {items[3]}, {items[4]}\n'
        return f'{query_result} \nКоличество записей {len(query_data)}'

    def get_avg_salary(self) -> str:
        """
        Получает среднюю зарплату по вакансиям.
        :return: Отформатированная для вывода строка с данными -> str
        """
        with self.__connection as conn:
            # Открываем курсор для работы с БД, с таблицей customers
            with conn.cursor() as cur:
                # Выполняем SQL-запрос
                cur.execute(f'SELECT AVG((salary_from + salary_to) / 2) FROM vacancy')
                # Получаем ответ и копируем его в переменную
                query_result = cur.fetchall()
            # Закрываем курсор
            cur.close()
        return f'Средняя зарплата (min+max)/2 = {int(query_result[0][0])}'

    def get_vacancies_with_higher_salary(self) -> str:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Отформатированная для вывода строка с данными -> str
        """
        query_result = ''
        with self.__connection as conn:
            # Открываем курсор для работы с БД, с таблицей customers
            with conn.cursor() as cur:
                # Выполняем SQL-запрос
                cur.execute(
                    f'SELECT * FROM vacancy '
                    f'WHERE ((salary_from + salary_to) / 2) > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancy)')
                # Получаем ответ и копируем его в переменную
                query_data = cur.fetchall()
            # Закрываем курсор
            cur.close()
        # Из полученных данных формируем результат в строковом формате с построчным переносом
        for items in query_data:
            query_result += f'{items[0]}, {items[1]}, {items[2]}, {items[3]}, {items[4]}, {items[5]}, {items[6]}\n'
        return f'{query_result} \nКоличество записей {len(query_data)}'

    def get_vacancies_with_keyword(self, user_query: str) -> str:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например “python”.
        :param user_query: Запрос пользователя -> str
        :return: Отформатированная для вывода строка с данными -> str
        """
        query_result = ''
        with self.__connection as conn:
            # Открываем курсор для работы с БД, с таблицей customers
            with conn.cursor() as cur:
                # Выполняем SQL-запрос
                cur.execute(
                    f'SELECT * FROM vacancy '
                    f"WHERE vacancy_name LIKE '%{user_query}%' OR vacancy_name LIKE '%{user_query.capitalize()}%'")
                # Получаем ответ и копируем его в переменную
                query_data = cur.fetchall()
            # Закрываем курсор
            cur.close()
        # Из полученных данных формируем результат в строковом формате с построчным переносом
        for items in query_data:
            query_result += f'{items[0]}, {items[1]}, {items[2]}, {items[3]}, {items[4]}, {items[5]}, {items[6]}\n'
        return f'{query_result} \nКоличество записей {len(query_data)}'

    def db_connection_close(self):
        """
        Закрывает соединение с БД
        """
        if not self.__connection.closed:
            self.__connection.close()
