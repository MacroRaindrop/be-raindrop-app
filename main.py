from typing import List
import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware

import services
services.create_database()

import sqlalchemy.orm as orm

import schemas


app = _fastapi.FastAPI()

@app.post("/companies", response_model=schemas.CompanyBase)
def create_company(company: schemas.CompanyCreate, db: orm.Session=_fastapi.Depends(services.get_db)):
    db_email= services.get_company_by_email(db=db, email=company.owner_email)
    if db_email:
        raise _fastapi.HTTPException(status_code=400, detail="the email is in use")
    return services.create_company(db=db, company=company)

@app.post("/login", response_model=schemas.CompanyBase)
def login_company(company: schemas.CompanyLogin, db: orm.Session=_fastapi.Depends(services.get_db)):
    db_company = services.get_company_by_email(db=db, email=company.owner_email)
    if not db_company:
        raise _fastapi.HTTPException(status_code=400, detail="the company is not found")
    if db_company.owner_password!=company.owner_password:
        raise _fastapi.HTTPException(status_code=401, detail="the password is incorrect")
    db_company = schemas.CompanyBase(
        id=db_company.id,
        created_at=db_company.created_at,
        owner_name=db_company.owner_name,
        name=db_company.name,
        owner_email=db_company.owner_email,
        owner_password=db_company.owner_password
    )
    return db_company

@app.post("/products", response_model=schemas.ProductBase)
def create_product(product: schemas.ProductCreate, db: orm.Session=_fastapi.Depends(services.get_db)):
    return services.create_product(db=db, product=product)

@app.get("/products", response_model=List[schemas.ProductBase])
def get_products(skip: int = 0, limit: int = 10, db: orm.Session=_fastapi.Depends(services.get_db)):
    products = services.get_products(db=db, skip=skip, limit=limit)
    print(products)
    return products

@app.get("/products/{product_id}", response_model=schemas.ProductBase)
def get_product(product_id: int, db: orm.Session=_fastapi.Depends(services.get_db)):
    product = services.get_product(id=product_id, db=db)
    if product is None:
        raise _fastapi.HTTPException(status_code=400, detail="maaf product tidak ditemukan")
    return product

@app.get("/products-user/{user_id}", response_model=List[schemas.ProductBase])
def get_products_by_user(user_id: int, db: orm.Session=_fastapi.Depends(services.get_db)):
    print(user_id)
    product = services.get_products_by_user(id=user_id, db=db)
    if product is None:
        raise _fastapi.HTTPException(status_code=400, detail="maaf product tidak ditemukan")
    return product

@app.put("/products", response_model=schemas.ProductBase)
def create_product(product: schemas.ProductCreate, db: orm.Session=_fastapi.Depends(services.get_db)):
    return services.update_product(db=db, product=product)