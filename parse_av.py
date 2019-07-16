# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup as bs


BASE_URL = 'https://cars.av.by/infiniti'
#https://cars.av.by/jaguar
#https://cars.av.by/infiniti


def get_html(url):
    request = requests.get(url)
    request.encoding = 'utf-8'
    return request.text   
    

def get_page_count(html):
    soup = bs(html, 'lxml')
    count = soup.find('li', class_ = 'pages-arrows-index').text[5:]    
    return int(count)

    
def parse(html):
    soup = bs(html, 'lxml')
    divs = soup.find_all('div', attrs = {'class':'listing-item'})

    avtos = []
    for div in divs:
        
        href = div.find('div', attrs = {'class':'listing-item-title'}).find('a')['href']
        model = div.find('div', attrs = {'class':'listing-item-title'}).find('a').text.strip()
        year = div.find('div', attrs = {'class':'listing-item-price'}).contents[1].text + 'г'
        price = div.find('strong').contents[0] + 'р.'
        avtos.append({'url' : href,
                     'model': model,
                     'year' : year,
                     'price': price})
    return avtos
    

def save(avtos, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Проект', 'Категории', 'Цена', 'Заявки'))

        writer.writerows(
            (avto['model'], avto['price'], avto['year'], avto['url']) for avto in avtos
        )
    return True


def main():
    path = 'avto.csv'
    project = []
    
    count_page = get_page_count(get_html(BASE_URL))
    print('Количество страниц {0}'.format(count_page))
    
    for page in range(1, count_page + 1):
        print('Парсинг {0}% ({1}/{2})'.format(page / count_page * 100, page, count_page))
        project.extend(parse(get_html(BASE_URL + "/page/{0}".format(page))))
        
    print('{0} avto'.format(len(project)))
    print('Сохранение...')
    
    if save(project, path):
        print('__Готово__')
    else: 
        print('__ERROR__')
            
  
if __name__ == '__main__':
    main()
