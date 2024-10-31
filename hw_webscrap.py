import requests
from bs4 import BeautifulSoup
import json
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
main_url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

main_response = requests.get(main_url, headers=headers)
main_html = main_response.text
main_soup = BeautifulSoup(main_html, "lxml")
main_tag = main_soup.find('main', class_="vacancy-serp-content")
vacancy_card = main_tag.find_all("div", class_="magritte-redesign")

vacancies = []
for vacancy_tag in vacancy_card:
    h2_tag = vacancy_tag.find("h2", class_="bloko-header-section-2")
    title = h2_tag.text.strip() if h2_tag else "Заголовок отсутствует"

    salary_tag = vacancy_tag.find("span", {"data-sentry-component": "Compensation"})
    salary = salary_tag.text.strip() if salary_tag else "Зарплатная вилка не указана"

    address_tag = vacancy_tag.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
    address = address_tag.text.strip() if address_tag else "Адрес не указан"

    company_tag = vacancy_tag.find("span", {"data-qa": "vacancy-serp__vacancy-employer-text"})
    company = company_tag.text.strip() if company_tag else "Название компании не указано"

    vacancy_url = vacancy_tag.find("a", {"data-qa": "serp-item__title"})["href"]
    vacancy_info = requests.get(vacancy_url, headers=headers)
    vacancy_html = vacancy_info.text
    vacancy_soup = BeautifulSoup(vacancy_html, "lxml")

    description = vacancy_soup.find("div", {"data-qa": "vacancy-description"}).text.lower()
    if "django" in description or "flask" in description:  
        vacancy_data = {
            "Vacancy URL": vacancy_url,
            "Title": title,
            "Salary": salary,
            "Company": company, 
            "Address": address}
        vacancies.append(vacancy_data)

    time.sleep(1)

with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print(f"Парсинг вакансий завершен. Данные о вакансиях сохранены в файл vacancies.json. Количество найденых вакансий: {len(vacancies)}")
