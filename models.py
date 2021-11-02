import sqlalchemy as _sql
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
import sqlalchemy.orm as _orm 
from sqlalchemy.orm import relationship

from database import Base

class Company(Base):
    __tablename__ = 'company'
    id              = Column(Integer, primary_key=True, index=True)
    created_at      = Column(DateTime)
    owner_name      = Column(String)
    name            = Column(String, unique=True, index=True)
    owner_email     = Column(String, unique=True, index=True)
    owner_password  = Column(String)
    products        = relationship("Product", back_populates="company")
    staff           = relationship("Staff", back_populates="company")
    histories       = relationship("History", back_populates="company")
    preorders       = relationship("Preorder", back_populates="company")
    logs            = relationship("Log", back_populates="company")

class Staff(Base):
    __tablename__ = 'staff'
    id              = Column(Integer, primary_key=True, index=True)
    created_at      = Column(DateTime)
    id_company      = Column(Integer, ForeignKey('company.id'))
    company         = relationship("Company", back_populates="staff")
    name            = Column(String)
    email           = Column(String, unique=True, index=True)
    password        = Column(String)
    role            = Column(String)
    preorders       = relationship("Preorder", back_populates="staff")
    logs            = relationship("Log", back_populates="staff")

class Product(Base):
    __tablename__ = 'product'
    id              = Column(Integer, primary_key=True, index=True)
    created_at      = Column(DateTime)
    id_company      = Column(Integer, ForeignKey('company.id'))
    company         = relationship("Company", back_populates="products")
    name            = Column(String, unique=True, index=True)
    minimum_stock   = Column(Integer)
    image           = Column(String)
    unit            = Column(Integer)
    descriptopn     = Column(String)
    quantity        = Column(Integer)
    histories       = relationship("History", back_populates="products")
    preorders       = relationship("Preorder", back_populates="products")

class History(Base):
    __tablename__ = 'history'
    id              = Column(String, primary_key=True)
    created_at      = Column(DateTime)
    id_company      = Column(Integer, ForeignKey('company.id'))
    company         = relationship("Company", back_populates="histories")
    id_product      = Column(Integer, ForeignKey('product.id'))
    products         = relationship("Product", back_populates="histories")
    inbound         = Column(String)
    outbound        = Column(Integer)
    unit            = Column(Integer)
    notes           = Column(String)

class Preorder(Base):
    __tablename__ = 'preorder'
    id              = Column(String, primary_key=True)
    created_at      = Column(DateTime)
    id_company      = Column(Integer, ForeignKey('company.id'))
    company         = relationship("Company", back_populates="preorders")
    id_product      = Column(Integer, ForeignKey('product.id'))
    products        = relationship("Product", back_populates="preorders")
    id_staff        = Column(Integer, ForeignKey('staff.id'))
    staff           = relationship("Staff", back_populates="preorders")
    supplier        = Column(String)
    date            = Column(String)
    quantity        = Column(Integer)

class Log(Base):
    __tablename__ = 'log'
    id              = Column(Integer, primary_key=True)
    created_at      = Column(DateTime)
    id_company      = Column(Integer, ForeignKey('company.id'))
    company         = relationship("Company", back_populates="logs")
    id_staff        = Column(Integer, ForeignKey('staff.id'))
    staff           = relationship("Staff", back_populates="logs")