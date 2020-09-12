import argparse
import csv
import datetime
import logging
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config

logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$') #https://example.com/hello
is_root_path = re.compile(r'^/.+$') # /algun-texto

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Iniciando scraper de {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('¡Articulo enlazado!')
            articles.append(article)
            break #Opcional para tomar solo el primer articulo

    _save_articles(news_site_uid, articles)

def _save_articles(news_site_uid, articles):
    hoy = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime=hoy)
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article,prop)) for prop in csv_headers]
            writer.writerow(row)

def _fetch_article(news_site_uid, host, link):
    logger.info('Comenzando a enlazar el articulo {}'.format(link))
    article = None

    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error enlazando el articulo', exc_info=False)
    if article and not article.body:
        logger.warning('Articulo invalido. No hay cuerpo')
        return None
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_sites'].keys())

    parser.add_argument('news_site',
                        help='Los sitios de noticias que quieres scrapear',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)