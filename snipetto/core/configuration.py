import os

SNIPETTO_HOST = os.environ.get('SNIPETTO_HOST', 'http://localhost:8000')
SNIPETTO_PATH_CONFIGURATION = '/v1/api/paths/'
HOME_DIR = os.path.expanduser('~')
CONFIG_PATH = '{}/.snippetto'.format(HOME_DIR)
