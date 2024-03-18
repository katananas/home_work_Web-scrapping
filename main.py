import requests
import random
import json
import lxml
from bs4 import BeautifulSoup
from fake_headers import Headers

url = 'https://spb.hh.ru/search/vacancy?text=django%2C+flask&salary=&area=1&area=2&ored_clusters=true'


def gen_headers():
    browser = random.choices(["chrome", "firefox", "opera"])[0]
    os = random.choices(["win", "mac", "lin"])[0]
    headers = Headers(browser=browser, os=os)
    return headers.generate()


# Функция которая получает список вакансий
def search():
    response = requests.get(url, headers=gen_headers())
    soup = BeautifulSoup(response.text, 'lxml')
    vacancies = soup.findAll('div', class_='vacancy-serp-item-body')
    data = []

    for vacancy in vacancies:
        link = vacancy.find('a', class_='bloko-link').get('href')
        position = vacancy.find('a', class_='bloko-link').text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-2').text.replace("\u202f", " ").replace("\xa0",
                                                                                                               " ")
        except:
            salary = 'нет информации о ЗП'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("\xa0", " ")
        location = vacancy.findAll('div', class_='bloko-text')[1].text.replace("\xa0", " ")

        # print(link, position, salary, company_name, location)

        data.append([link, position, salary, company_name, location])

    return data


# Функция преобразует список в словарь
def convert_to_dict(data):
    return [dict(zip(['link', 'position', 'salary', 'company_name', 'location'], row)) for row in data]


# Функция сохраняет список вакансий в json-файл
def write_json(data):
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    search()
    write_json(convert_to_dict(search()))