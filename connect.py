from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:12345@localhost:5432/postgres"


engine = create_engine(DATABASE_URL, echo=False)

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
