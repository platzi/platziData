import argparse
import logging
logging.basicConfig(level=logging.INFO)

import news_page_objects as news
from common import config


logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    logging.info('Finding links in homepage...')

    article_links = _find_article_links_in_homepage(news_site_uid)

    logging.info('{} article links found in homepage'.format(len(article_links)))
    for link in article_links:
        print(link)


def _find_article_links_in_homepage(news_site_uid):
    homepage = news.HomePage(news_site_uid)

    return homepage.article_links


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)

