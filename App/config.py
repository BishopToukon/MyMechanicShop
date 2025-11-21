import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:LucaAugust23@localhost/mymechanicshop"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

class ProductionConfig(Config):
    DEBUG = False
