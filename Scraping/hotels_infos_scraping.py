import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
import json
import time

cities_list = ["Mont+Saint+Michel", "Saint+Malo", "Bayeux", "Le+Havre", "Rouen", "Paris", "Amiens", "Lille", "Strasbourg", "Chateau+du+Haut+Koenigsbourg", "Colmar",
"Eguisheim", "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon", "Gorges+du+Verdon", "Bormes+les+Mimosas", "Cassis", "Marseille", "Aix+en+Provence",
"Avignon", "Uzes", "Nimes", "Aigues+Mortes", "Saintes+Maries+de+la+mer", "Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz",
"Bayonne", "La+Rochelle"]

for i in range(len(cities_list)):


    class HotelinfoSpider(scrapy.Spider):
        name = "link_hotel"

        with open("Scraping/hotels_links/hotel_links_{}.json".format(cities_list[i])) as f:
            urls = json.load(f)
            start_urls = [line['hotel_url'] for line in urls]

        def parse(self, response):
                time.sleep(0.3)
                yield {
                    "hotel_name" : response.css("h2[class='d2fee87262 pp-header__title']::text").get(),
                    "url_hotel" : response.url,
                    "hotel_coordinates" : response.css("a[id='map_trigger_header']::attr(data-atlas-latlng)").get(),
                    "score" : response.css("div[class='a3b8729ab1 d86cee9b25']::text").get().replace(',', '.'),
                    "text_description" : response.css("p[class='a53cbfa6de b3efd73f69']::text").get(),
                    "address" : response.css("div[class='a53cbfa6de f17adf7576']::text").get()
                    #"price_week" : response.css("span[class='prco-valign-middle-helper']::text").get().replace("\xa0", "").replace("\n", "")
                }
                


    filename = "hotels_infos_{}.json".format(cities_list[i])

    if filename in os.listdir('Scraping/hotels_infos_per_city/'):
                os.remove('Scraping/hotels_infos_per_city/'+filename)

    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': logging.INFO,
          'DEFAULT_REQUEST_HEADERS': {
        'Accept-Language': 'fr-FR,fr;q=0.9'
        },
        "FEEDS": {
            'Scraping/hotels_infos_per_city/'+filename : {"format": "json", "encoding": "utf-8",},
        },
        'DOWNLOAD_FAIL_ON_DATALOSS' : True,
        'RETRY_ENABLED' : True
    })

    process.crawl(HotelinfoSpider)
process.start()