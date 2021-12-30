from instance.config import MERCHANT_ID


class Config(object):
    MERCHANT_ID='kfjgu'

class ProductionConfig(Config):
    MERCHANT_ID='nsjgkhbyhiykmdfinvdngb'
    DATABASE_URI=''
    SECRET_KEY='Hz_Vq0XyJUJ6rbo'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'ogunyemiimotunrayo@gmail.com'
    MAIL_PASSWORD = ''
    MAIL_USE_SSL = True

class DevelopmentConfig(Config):
    DATABASE_URI=''