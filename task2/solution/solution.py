import csv
import re
from collections import defaultdict
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


def get_animals_wiki_first_page():
    wiki_animals_url = ('https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0'
                        '%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1'
                        '%82%D1%83')
    response = httpx.get(wiki_animals_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def return_verified_animal_titles(animals):
    animal_titles = []
    for animal in animals:
        if animal['title'] in ['Rhizostoma pulmo']:
            continue
        if not has_cyrillic(animal['title']):
            return animal_titles, True
        animal_titles.append(animal['title'])
    return animal_titles, False


def get_animals_wiki_letters_stats(soup):
    letter_stats = defaultdict(int)
    wiki_url = 'https://ru.wikipedia.org'
    while True:
        animals = soup.select('.mw-category-group ul')[2].select('li a')
        animal_titles, should_stop = return_verified_animal_titles(animals)
        for animal_title in animal_titles:
            first_letter = animal_title[0].upper()
            letter_stats[first_letter] += 1
        if should_stop:
            break
        next_link = soup.find('a', string='Следующая страница')
        if not next_link:
            break
        next_page_url = next_link['href']
        page_url = urljoin(wiki_url, f'{next_page_url}')
        response = httpx.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
    return letter_stats


def write_to_csv(file_name, write_data):
    with open(f'{file_name}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(write_data)


if __name__ == '__main__':
    file_name_path = 'task2/beasts.csv'
    animals_wiki_first_page = get_animals_wiki_first_page()
    letter_stats = get_animals_wiki_letters_stats(animals_wiki_first_page)
    converted_data_for_csv = [[key, value] for key, value in letter_stats.items()]
    write_to_csv(file_name_path, converted_data_for_csv)
