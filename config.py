import string
import random

random_string = string.ascii_letters + string.digits + string.ascii_uppercase
DEBUG = True
MYSQL_DB = 'booh3ea84eak40eq7jcp'
MYSQL_HOST = 'booh3ea84eak40eq7jcp-mysql.services.clever-cloud.com'
MYSQL_PASSWORD = 'DkvdhNuKodIuGtFRxAuX'
MYSQL_PORT = '3306'
MYSQL_USER = 'utbhj4gmmyroc07r'
MYSQL_URI = (
    'mysql://'
    f'{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
)
SQLALCHEMY_DATABASE_URI = MYSQL_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = ''.join(random.choice(random_string) for i in range(9))
