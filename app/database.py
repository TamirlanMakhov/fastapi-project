from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# raw-sql
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',
    #         database=settings.database_name,
    #         user=settings.database_username,
    #         password=settings.database_password)
#         cursor = conn.cursor()
#         print('success')
#         break
#     except psycopg2.OperationalError as ex:
#         print('Connection to db failed')
#         time.sleep(2)
