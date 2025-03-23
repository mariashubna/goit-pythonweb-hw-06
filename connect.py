from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


engine = create_engine("postgresql://postgres:12345@localhost:5432/HW6-postgres")

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
