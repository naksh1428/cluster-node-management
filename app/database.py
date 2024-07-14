import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Load environment variables from the .env file (if present)
load_dotenv()
user = os.getenv('MYSQL_USER')
creds = os.getenv('MYSQL_PASSWORD')
user_db = os.getenv('MYSQL_DATABASE')


"""docker container Database URL"""
URL_DATABASE = f'mysql+pymysql://{user}:{creds}@db:3306/{user_db}'

"""local host Database URL"""
#URL_DATABASE = f'mysql+pymysql://{user}:{creds}@localhost:3306/mydb'


engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
