from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import sqlalchemy.ext.declarative as _declarative
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "postgres://arlbteehpdfpcv:664de19fadbd55a9eda1cb3ea593c874003362a37ac6c9cc31ea3e3bd9867b50@ec2-34-202-178-115.compute-1.amazonaws.com:5432/d16ehj7c9cm6gi"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @as_declarative()
# class Base:

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

Base = _declarative.declarative_base()