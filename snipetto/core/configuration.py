import os

SNIPPETTO_HOST = os.environ.get('SNIPPETTO_HOST', 'http://localhost:8000')
SNIPPETTO_PATH_CONFIGURATION = '/v1/api/paths/'
HOME_DIR = os.path.expanduser('~')
CONFIG_PATH = '{}/.snippetto'.format(HOME_DIR)
