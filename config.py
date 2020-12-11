class Config:

    DEBUG = True

    #"pepo" tilalle oman pgadmin4 käyttäjän nimi ja "password" tilalle sen käyttäjän salasana.
    #"tilanvaraus" tilalle luodun tietokannan nimi
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:password@localhost/tilanvaraus'

    #Ei toiminu flask db migrate ennenkun tein uuden käyttäjän "test" ja annoin sille oikeuden "log in" ja päivitin sen database uriin. //pessi Oli joku bugi vissii :))))))))))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'password'
