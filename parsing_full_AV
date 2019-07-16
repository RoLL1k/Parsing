 #-*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool


BASE_URL = 'https://av.by'
path = 'avto.csv'


def get_html(url):
	request = requests.get(url)
	request.encoding = 'utf-8'
	return request.text 


def get_allbrands_urls(url):
	soup = bs(get_html(url), 'lxml')
	uls = soup.find('ul', attrs = {'class':'brandslist'}).find_all('li', attrs = {'class':'brandsitem'})
	urls = []
	for ul in uls:
		urls.append(ul.find('a').get('href'))
	return urls


def get_page_count(url):
	soup = bs(get_html(url), 'lxml')
	count = soup.find('li', attrs = {'class':'pages-arrows-index'})

	if count == None:
		count = 1
	else:
		count = int(count.text[5:])
	
	pages = []
	pages.append(url)

	for i in range(2, count + 1):
		pages.append(url + "/page/{0}".format(i))
	return pages

	
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
	

def save(avtos):
	with open(path, 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('_'*25).split(','))
		writer.writerows(
		 		(avto['model'], avto['price'], avto['year'], avto['url']) for avto in avtos
		 	)


def make_all(pages):
	avtos = parse(get_html(pages))
	save(avtos)
	
	
def main():
	urls = get_allbrands_urls(BASE_URL)

	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Модель', 'Цена', 'Год', 'Ссылка'))

		for url in urls:
			model_urls = get_allbrands_urls(url)
			print('parsing...' + url + '...')
			for model_url in model_urls:
				pages = get_page_count(model_url)
				with Pool(40) as p:
					p.map(make_all, pages)
	
			 
if __name__ == '__main__':
	main()
