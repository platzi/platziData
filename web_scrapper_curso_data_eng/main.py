# necesita el metodo config() de common.py para cargar la información de config.yaml.
# >> main.py -h muestra las fuentes de información validas.
# >> main.py [fuente de información] ejemplo: main.py semana
# esto se hace con el fin de obtener la url de la fuente.

import argparse
import logging
logging.basicConfig(level=logging.INFO)

import news_page_objects as news
from common import config

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Iniciando scraper de {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)

    for link in homepage.article_links:
        print(link)

if __name__ == '__main__':
    news_site_choices = list(config()['news_sites'].keys())

    parser = argparse.ArgumentParser()
    parser.add_argument('news_site',
                        help='Los sitios de noticias que quieres scrapear',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)