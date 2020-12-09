class Config:

    DEBUG = True

    #"pepo" tilalle oman pgadmin4 käyttäjän nimi ja "password" tilalle sen käyttäjän salasana.
    #"tilanvaraus" tilalle luodun tietokannan nimi
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pepo:password@localhost:5050/tilanvaraus'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'password'
