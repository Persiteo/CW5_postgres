# Курсовая работа 5. Работа с базами данных.

Программа через API HeadHunter получает данные о 10 организациях и вакансиях этих организаций
и записывает эти данные в таблицы базы данных headhunter в Postgres.
Программа позволят делать запросы к данным в БД:

- Список всех компаний и количество вакансий у каждой компании
- Список всех вакансий с названием компании, вакансии, зарплаты и ссылки на вакансию
- Средняя зарплата по вакансиям
- Список всех вакансий, у которых зарплата выше средней по всем вакансиям
- Список всех вакансий по ключевому слову в названии

## Требования к окружению

#### В программе используется менеджер зависимостей Poetry.
Используются следующие зависимости:
- python = "^3.11"
- requests = "^2.31.0"
- psycopg2 = "^2.9.6"

## Требования к установке
Для корректной работы необходимо создать в Postgres базу данных headhunter
```
CREATE DATABASE headhunter;
```
В созданной базе данных необходимо создать 2 таблицы - vacancy и company
```
CREATE TABLE company
(
	company_id int PRIMARY KEY,
	company_name varchar,
	company_city varchar,
	company_site_url varchar,
	company_hh_url varchar,
	company_description text
);

CREATE TABLE vacancy
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar,
	company_id int REFERENCES company(company_id) NOT NULL,
	salary_from	real,
	salary_to real,
	vacancy_url varchar,
	vacancy_description text
);
```

