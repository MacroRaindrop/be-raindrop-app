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

class CompanyCreate(BaseModel):
    owner_name      :str = Field(..., example="agnii")
    name            :str = Field(..., example="raindrop corp.")
    owner_email     :str = Field(..., example="agni@raindrop.app")
    owner_password  :str = Field(..., example="agniganteng")

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

    class config: 
        orm_mode: True

class StaffCreate(BaseModel):
    id_company      :str = Field(..., example="089asdf89h920")
    name            :str = Field(..., example="agni")
    email           :str = Field(..., example="agni@raindrop.app")
    password        :str = Field(..., example="agniganteng")
    role            :str = Field(..., example="bosq")

class Staff(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    name                :str
    email               :str
    role                :str

    class config: 
        orm_mode: True

class ProductBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    name                :str
    minimum_stock       :int
    image               :str
    unit                :str
    description         :str
    quantity            :int

    class config: 
        orm_mode: True

class ProductCreate(BaseModel):
    id_company      :int = Field(..., example=1)
    name            :str = Field(..., example="shampoo")
    minimum_stock   :int = Field(..., example=10)
    image           :str = Field(..., example="https://asd.com/img.png")
    unit            :str = Field(..., example="buah")
    description     :str = Field(..., example="shampoonya anggun")
    quantity        :int = Field(..., example=100)

class HistoryBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    id_product          :str
    inbound             :int
    outbound            :int
    unit                :str
    notes               :str

    class config: 
        orm_mode: True

class HistoryCreate(BaseModel):
    id_company      :str = Field(..., example="089asdf89h920")
    id_product      :str = Field(..., example="8asd09882")
    inbound         :int = Field(..., example=100)
    outbound        :int = Field(..., example=0)
    unit            :str = Field(..., example="buah")
    notes           :str = Field(..., example="inbound dari toko x")

class PreOrderBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    id_product          :str
    id_staff            :str
    supplier            :str
    date                :str
    quantity            :int

    class config: 
        orm_mode: True

class PreOrderCreate(BaseModel):
    id_company      :str = Field(..., example="089asdf89h920")
    id_product      :str = Field(..., example="8asd09882")
    id_staff        :str = Field(..., example="asd89hf9n2")
    supplier        :str = Field(..., example="toko x")
    date            :str = Field(..., example="2021-11-11")
    quantity        :int = Field(..., example=100)

class LogBase(BaseModel):
    id                  :str
    created_at          :datetime
    id_company          :str
    id_staff            :str

    class config: 
        orm_mode: True

class LogCreate(BaseModel):
    id_company      :str = Field(..., example="089asdf89h920")
    id_staff        :str = Field(..., example="asd89hf9n2")
