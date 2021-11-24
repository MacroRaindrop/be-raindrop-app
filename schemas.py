from database import Base
import pydantic as _pydantic
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class CompanyBase(BaseModel):
    id: int
    created_at: datetime
    owner_name: str
    name: str
    owner_email: str
    owner_password: str

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    owner_name: str
    name: str
    owner_email: str
    owner_password: str


class Company(BaseModel):
    id: int
    created_at: datetime
    owner_name: str
    name: str
    owner_email: str


class CompanyLogin(BaseModel):
    owner_email: str
    owner_password: str


class StaffBase(BaseModel):
    id: int
    created_at: datetime
    id_company: str
    name: str
    email: str
    password: str
    role: str

    class Config:
        orm_mode = True


class StaffCreate(BaseModel):
    id_company: int
    name: str
    email: str
    password: str
    role: str


class Staff(BaseModel):
    id: int
    created_at: datetime
    id_company: str
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    id: int
    created_at: datetime
    id_company: int
    name: str
    minimum_stock: int
    image: str
    unit: str
    description: str
    quantity: int

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    id_company: int
    name: str
    minimum_stock: int
    image: str
    unit: str
    description: str
    quantity: int


class HistoryBase(BaseModel):
    id: int
    created_at: datetime
    id_company: int
    id_product: int
    inbound: int
    outbound: int
    unit: str
    notes: str

    class Config:
        orm_mode = True


class HistoryCreate(BaseModel):
    id_company: int
    id_product: int
    inbound: int
    outbound: int
    notes: str


class PurchaseOrderBase(BaseModel):
    id: int
    created_at: datetime
    id_purchaseorder: int
    id_company: int
    id_staff: int
    supplier: str
    date: str

    class Config:
        orm_mode = True


class PurchaseOrderDetailBase(BaseModel):
    id: int
    id_company: int
    id_purchaseorder: int
    id_product: int
    quantity: int

    class Config:
        orm_mode = True


class PurchaseOrderDetailCreate(BaseModel):
    id_product: int
    quantity: int


class PurchaseOrderCreate(BaseModel):
    id_company: int
    id_staff: int
    supplier: str
    date: str
    products: List[PurchaseOrderDetailCreate]


class PurchaseOrderDetailResponse(BaseModel):
    id_purchaseorder: int
    id_company: int
    id_staff: int
    supplier: str
    date: str
    products: List[PurchaseOrderDetailCreate]


class InboundCreate(BaseModel):
    id_company: int
    id_purchaseorder: int
    products: List[PurchaseOrderDetailCreate]
    notes: str


class LogBase(BaseModel):
    id: int
    created_at: datetime
    id_company: int
    id_staff: int

    class Config:
        orm_mode = True


class LogCreate(BaseModel):
    id_company: int
    id_staff: int
