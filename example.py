import logging
from config import *
from pynoovo import Noovo

logging.basicConfig(
  format='%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
  datefmt='%Y-%m-%d,%H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


noovo = Noovo(
  cache_dir = cache_dir,
  username  = username,
  password  = password,
  site = site
  )

search_result = noovo.search("roast")
serie_infos = noovo.get_result_infos(search_result[0])
play_infos_serie = noovo.get_play_infos(serie_infos['fr'], season = 4, episode = 1)
categories = noovo.get_root_categories()
serie_category = noovo.get_elements(categories[0])
drames_category = noovo.get_elements(serie_category[0])
collection_category = noovo.get_elements(categories[4])

search_result = noovo.search("your honor")
serie_infos = noovo.get_result_infos(search_result[0])

search_result = noovo.search("justice league")
movie_infos = noovo.get_result_infos(search_result[0])
account = noovo.get_account_infos()

play_infos_serie = noovo.get_play_infos(serie_infos['fr'], season = 1, episode = 1)

logger.info('Manifest: {}'.format(play_infos_serie.manifest_url))
logger.info('License URL: {}'.format(play_infos_serie.license_url))
play_infos_serie = noovo.get_play_infos(serie_infos['en'], season = 1, episode = 1)
logger.info('Manifest: {}'.format(play_infos_serie.manifest_url))
logger.info('License URL: {}'.format(play_infos_serie.license_url))

play_infos_movie = noovo.get_play_infos(movie_infos['fr'])
logger.info('Manifest: {}'.format(play_infos_movie.manifest_url))
logger.info('License URL: {}'.format(play_infos_movie.license_url))