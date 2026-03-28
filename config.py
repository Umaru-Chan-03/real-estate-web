class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://tupn:123456@127.0.0.1/real_estate"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "super-secret-key"

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "123456"