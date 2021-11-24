import sqlalchemy as _sql
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, PrimaryKeyConstraint
import sqlalchemy.orm as _orm
from sqlalchemy.orm import relationship

from database import Base


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    owner_name = Column(String)
    name = Column(String)
    owner_email = Column(String, unique=True, index=True)
    owner_password = Column(String)
    products = relationship("Product", back_populates="company")
    staff = relationship("Staff", back_populates="company")
    histories = relationship("History", back_populates="company")
    purchaseorders = relationship("Purchaseorder", back_populates="company")
    purchaseorderdetails = relationship(
        "PurchaseorderDetail", back_populates="company")
    logs = relationship("Log", back_populates="company")


class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    id_company = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="staff")
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    purchaseorders = relationship("Purchaseorder", back_populates="staff")
    logs = relationship("Log", back_populates="staff")


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    id_company = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="products")
    name = Column(String)
    minimum_stock = Column(Integer)
    image = Column(String)
    unit = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    histories = relationship("History", back_populates="products")
    purchaseorderdetails = relationship(
        "PurchaseorderDetail", back_populates="products")

    def __eq__(self, other):
        return self.id == other.id


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    id_company = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="histories")
    id_product = Column(Integer, ForeignKey('product.id'))
    products = relationship("Product", back_populates="histories")
    inbound = Column(String)
    outbound = Column(Integer)
    notes = Column(String)


class Purchaseorder(Base):
    __tablename__ = 'purchaseorder'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    id_purchaseorder = Column(Integer)
    id_company = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="purchaseorders")
    id_staff = Column(Integer, ForeignKey('staff.id'))
    staff = relationship("Staff", back_populates="purchaseorders")
    supplier = Column(String)
    date = Column(String)
    purchaseorderdetails = relationship(
        "PurchaseorderDetail", back_populates="purchaseorders")


class PurchaseorderDetail(Base):
    __tablename__ = 'purchaseorder_detail'
    id = Column(Integer, primary_key=True, index=True)
    id_company = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="purchaseorderdetails")
    id_purchaseorder = Column(Integer, ForeignKey('purchaseorder.id'))
    purchaseorders = relationship(
        "Purchaseorder", back_populates="purchaseorderdetails")
    id_product = Column(Integer, ForeignKey('product.id'))
    products = relationship("Product", back_populates="purchaseorderdetails")
    quantity = Column(Integer)


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    id_company = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="logs")
    id_staff = Column(Integer, ForeignKey('staff.id'))
    staff = relationship("Staff", back_populates="logs")
