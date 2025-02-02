import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector

cities_list = ["Mont+Saint+Michel", "Saint+Malo", "Bayeux", "Le+Havre", "Rouen", "Paris", "Amiens", "Lille", "Strasbourg", "Chateau+du+Haut+Koenigsbourg", "Colmar",
"Eguisheim", "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon", "Gorges+du+Verdon", "Bormes+les+Mimosas", "Cassis", "Marseille", "Aix+en+Provence",
"Avignon", "Uzes", "Nimes", "Aigues+Mortes", "Saintes+Maries+de+la+mer", "Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz",
"Bayonne", "La+Rochelle"]

for i in range(len(cities_list)):

    class LinkSpider(scrapy.Spider):
        name = "link_hotel"

        start_urls = [
            "https://www.booking.com/searchresults.html?ss={}&nflt=ht_id=204".format(cities_list[i]),
        ]

        def parse(self, response):
                hotels = response.css("div[class='c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4']")
                for hotel in hotels:
                    hotel_url = hotel.css("a[class='a78ca197d0']").attrib["href"]
                    yield {
                        'hotel_url': hotel_url
                    }



    filename = "hotel_links_{}.json".format(cities_list[i])

    if filename in os.listdir('Scraping/hotels_links/'):
                os.remove('Scraping/hotels_links/'+filename)

    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            'Scraping/hotels_links/'+filename : {"format": "json"},
        },
        'DOWNLOAD_FAIL_ON_DATALOSS' : True,
        'RETRY_ENABLED' : True
    })

    process.crawl(LinkSpider)
process.start()