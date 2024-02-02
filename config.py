import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:<password>@localhost/dropbox_service_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'