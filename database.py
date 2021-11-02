from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import sqlalchemy.ext.declarative as _declarative
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "postgresql://nvazmfctihttdo:fe1113f960fee9957c99b733975b77c9ad324a0723a20219153be7f83be55621@ec2-54-87-92-21.compute-1.amazonaws.com:5432/d37noquh5kj5dt"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @as_declarative()
# class Base:

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

Base = _declarative.declarative_base()