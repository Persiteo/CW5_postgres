from src.headhunter_class import HeadHunterApi
from src.dbmanager_class import DBManager


EMPLOYERS_DATA = {1740: "Яндекс", 1111058: "Rockit", 9187006: "Answeroom", 250: "Comtec Inc", 67611: "Тензор",
                  3177: "ПервыйБит", 1455: "HeadHunter", 906557: "СберТех", 41862: "Контур", 733: "Artezio"}
VACANCY_SQL_FILTER = ['vacancy', "(%s, %s, %s, %s, %s, %s, %s)"]
COMPANY_SQL_FILTER = ['company', "(%s, %s, %s, %s, %s, %s)"]

db = DBManager()


# Функция взаимодействия с пользователем

def user_interaction() -> None:
    """
    Экран выбора api для пользователя
    :return: None
    """
    if db.init_error:
        exit()
    while True:
        print(f'==================================================================================')
        print(f'Добро пожаловать в программу работы с вакансиями с сайта HeadHunter')
        print(f'"1" - Получить данные по вакансиям и работодателям и записать в БД')
        print(f'"2" - Работа с данными БД')
        answer = input('Введите Exit для выхода\n')

        if answer.lower() not in ("1", "2", "exit"):
            print('Некорректный ввод, проверьте раскладку клавиатуры и введите один из предлагаемых вариантов\n')
        else:
            if answer == '1':
                hh = HeadHunterApi(EMPLOYERS_DATA)
                hh.get_vacancies_from_hh()
                vacancies_list = hh.get_vacancies_items()
                hh.get_employee_data()
                employee_list = hh.get_employee_items()
                db.insert_data_into_db(COMPANY_SQL_FILTER, employee_list)
                db.insert_data_into_db(VACANCY_SQL_FILTER, vacancies_list)

            elif answer == '2':
                second_menu()

            else:
                db.db_connection_close()
                exit()


def second_menu() -> None:
    while True:
        print("=======================================================================================")
        print(f"Работа с вакансиями, Ваши действия:")
        print(f"1 - Список всех компаний и количество вакансий у каждой компании")
        print(f"2 - Список всех вакансий с названием компании, вакансии, зарплаты и ссылки на вакансию")
        print(f"3 - Средняя зарплата по вакансиям")
        print(f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print(f"5 - Список всех вакансий по ключевому слову в названии")
        answer = input('Введите Exit для выхода\n')

        if answer.lower() in ("1", "2", "3", "4", "5", "exit"):
            if answer == "1":
                print(db.get_companies_and_vacancies_count())

            elif answer == "2":
                print(db.get_all_vacancies())

            elif answer == "3":
                print(db.get_avg_salary())

            elif answer == "4":
                print(db.get_vacancies_with_higher_salary())

            elif answer == "5":
                vacancy_keyword = input('Введите слово для поиска:\n')
                print(db.get_vacancies_with_keyword(vacancy_keyword))

            else:
                db.db_connection_close()
                exit()
        else:
            print('Некорректный ввод, проверьте раскладку клавиатуры и введите один из предлагаемых вариантов\n')


if __name__ == "__main__":
    user_interaction()
