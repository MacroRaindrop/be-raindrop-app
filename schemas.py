import pydantic as _pydantic
from pydantic import BaseModel, Field
from datetime import datetime

class CompanyBase(BaseModel):
    id                  :str
    created_at          :datetime
    owner_name          :str
    name                :str
    owner_email         :str
    owner_password      :str

    class Config:
        orm_mode = True

class CompanyCreate(BaseModel):
    owner_name      :str
    name            :str
    owner_email     :str
    owner_password  :str

class Company(BaseModel):
    id                  :str
    created_at          :datetime
    owner_name          :str
    name                :str
    owner_email         :str

class CompanyLogin(BaseModel):
    owner_email         :str
    owner_password      :str


class StaffBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    name                :str
    email               :str
    password            :str
    role                :str

    class Config:
        orm_mode = True

class StaffCreate(BaseModel):
    id_company      :str
    name            :str
    email           :str
    password        :str
    role            :str

class Staff(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    name                :str
    email               :str
    role                :str

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    id                  :int
    created_at          :datetime
    id_company          :int
    name                :str
    minimum_stock       :int
    image               :str
    unit                :str
    description         :str
    quantity            :int

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    id_company      :int
    name            :str
    minimum_stock   :int
    unit            :str
    description     :str
    quantity        :int

class HistoryBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    id_product          :str
    inbound             :int
    outbound            :int
    unit                :str
    notes               :str

    class Config:
        orm_mode = True

class HistoryCreate(BaseModel):
    id_company      :str
    id_product      :str
    inbound         :int
    outbound        :int
    unit            :str
    notes           :str

class PreOrderBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    id_product          :str
    id_staff            :str
    supplier            :str
    date                :str
    quantity            :int

    class Config:
        orm_mode = True

class PreOrderCreate(BaseModel):
    id_company      :str
    id_product      :str
    id_staff        :str
    supplier        :str
    date            :str
    quantity        :int

class LogBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    id_staff            :str

    class Config:
        orm_mode = True

class LogCreate(BaseModel):
    id_company      :str
    id_staff        :str
