import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
main_url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
parsed_data = []
keywords = ["Django", "Flask"]

main_response = requests.get(url=main_url, headers=headers)
main_html = main_response.text

main_soup = BeautifulSoup(main_html, features="lxml")
main_tag = main_soup.find('main', class_="vacancy-serp-content")

vacancy_card = main_tag.find_all("div", class_="magritte-redesign")

for vacancy_tag in vacancy_card:
    h2_tag = vacancy_tag.find("h2", class_="bloko-header-section-2")
    title = h2_tag.text.strip() if h2_tag else "Заголовок не найден"

    address_tag = vacancy_tag.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
    address = address_tag.text.strip() if address_tag else "Адрес не найден"

    parsed_data.append({
        "Title": title,
        "Address": address
        })
    
print(parsed_data)


vacancy_links = []
for vacancy_tag in main_soup.find_all("a", {"data-qa": "serp-item__title"}):
    vacancy_url = vacancy_tag["href"]
    vacancy_links.append(vacancy_url)
    