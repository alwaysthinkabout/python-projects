DOMAIN = 'electricity-bill'

ENV = 'production'
DEBUG = False
SECRET_KEY = 'this is a secret'

DEBUG_LOG = 'logs/debug.log'
ERROR_LOG = 'logs/error.log'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:635310@localhost:3306/electricity-bill'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

ORACLE_DATABASE_URI = 'hlcx/abc#123@10.150.182.228/SJHL'

ADMINS = []

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''

INCREMENTAL_SYNC_DATES = [13, 28]
INCREMENTAL_SYNC_TIME = '02:00'
CURRENT_QF_SYNC_TIME = '04:00'

SNYC_CONFIG_PATH = 'E:\\github\\project\\electricity-bill\\app\\sync.conf'
