

-- Создание БД headhunter
CREATE DATABASE headhunter;

-- Создание таблиц БД headhunter
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


-- Получает список всех компаний и количество вакансий у каждой компании.
SELECT DISTINCT company_name, COUNT(*) FROM company
LEFT JOIN vacancy ON vacancy.company_id=company.company_id
GROUP BY company_name

-- Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT company_name, vacancy_name, salary_from, salary_to, vacancy_url FROM company
INNER JOIN vacancy ON vacancy.company_id=company.company_id

-- Получает среднюю зарплату по вакансиям.
SELECT AVG((salary_to + salary_from) / 2) FROM vacancy


--получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT * FROM vacancy
WHERE ((salary_from + salary_to) / 2) > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancy)

-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
SELECT * FROM vacancy
WHERE vacancy_name LIKE '%Python%' OR vacancy_name LIKE '%python%'