import schemas
import sqlalchemy.orm as orm
from typing import List
import fastapi as _fastapi
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import services
services.create_database()


app = _fastapi.FastAPI()


@app.get("/", response_class=HTMLResponse)
def get_root():
    return """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BE services of Mavible by Raindrop</title>
    </head>
    <body>
        <h1>Welcome to BE Services of Mavible by Raindrop</h1>
        <a href="https://be-raindrop-app.herokuapp.com/redoc">API Documentation</a>
        <br/>
        <a href="https://be-raindrop-app.herokuapp.com/docs">Interactive API Documentation</a>
    </body>
    </html>"""


@app.post("/companies", response_model=schemas.CompanyBase)
def create_company(company: schemas.CompanyCreate, db: orm.Session = _fastapi.Depends(services.get_db)):
    db_email = services.get_company_by_email(db=db, email=company.owner_email)
    if db_email:
        raise _fastapi.HTTPException(
            status_code=400, detail="the email is in use")
    return services.create_company(db=db, company=company)


@app.post("/login", response_model=schemas.CompanyBase)
def login_company(company: schemas.CompanyLogin, db: orm.Session = _fastapi.Depends(services.get_db)):
    db_company = services.get_company_by_email(
        db=db, email=company.owner_email)
    if not db_company:
        raise _fastapi.HTTPException(
            status_code=400, detail="the company is not found")
    if db_company.owner_password != company.owner_password:
        raise _fastapi.HTTPException(
            status_code=401, detail="the password is incorrect")
    db_company = schemas.CompanyBase(
        id=db_company.id,
        created_at=db_company.created_at,
        owner_name=db_company.owner_name,
        name=db_company.name,
        owner_email=db_company.owner_email,
        owner_password=db_company.owner_password
    )
    return db_company


@app.get("/company-pic")
def get_company_pic(company_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    pic = services.get_company_by_id(db=db, id=company_id)
    return pic.owner_name


@app.get("/products", response_model=List[schemas.ProductBase])
def get_products(skip: int = 0, limit: int = 10, db: orm.Session = _fastapi.Depends(services.get_db)):
    products = services.get_products(db=db, skip=skip, limit=limit)
    print(products)
    return products


@app.get("/products/{product_id}", response_model=schemas.ProductBase)
def get_product(product_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    product = services.get_product(id=product_id, db=db)
    if product is None:
        raise _fastapi.HTTPException(
            status_code=400, detail="maaf product tidak ditemukan")
    return product


@app.get("/products-user/{user_id}", response_model=List[schemas.ProductBase])
def get_products_by_user(user_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    product = services.get_products_by_user(id=user_id, db=db)
    if product is None:
        raise _fastapi.HTTPException(
            status_code=400, detail="maaf product tidak ditemukan")
    return product


@app.post("/products", response_model=schemas.ProductBase)
def create_product(product: schemas.ProductCreate, db: orm.Session = _fastapi.Depends(services.get_db)):
    return services.create_product(db=db, product=product)


@app.put("/products", response_model=schemas.ProductBase)
def update_product(product: schemas.ProductBase, db: orm.Session = _fastapi.Depends(services.get_db)):
    return services.update_product(db=db, product=product)


@app.delete("/products/{product_id}", response_model=schemas.ProductBase)
def delete_product(product_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    product = services.delete_product(id=product_id, db=db)
    if product is None:
        raise _fastapi.HTTPException(
            status_code=400, detail="maaf product tidak ditemukan")
    return product


@app.get("/company-staff", response_model=List[schemas.StaffBase])
def get_company_staff(company_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    return services.get_staff(id=company_id, db=db)


@app.post("/staff", response_model=schemas.StaffBase)
def create_staff(staff: schemas.StaffCreate, db: orm.Session = _fastapi.Depends(services.get_db)):
    return services.create_staff(staff=staff, db=db)


@app.post("/purchaseorders", response_model=schemas.PurchaseOrderDetailResponse)
def create_purchaseorder(purchaseorder: schemas.PurchaseOrderCreate, db: orm.Session = _fastapi.Depends(services.get_db)):
    return services.create_purchaseorder(purchaseorder=purchaseorder, db=db)


@app.get("/purchaseorders", response_model=List[schemas.PurchaseOrderBase])
def get_purchaseorders_by_company(company_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    purchaseorders = services.get_purchaseorders(db=db, id=company_id)
    if not purchaseorders:
        raise _fastapi.HTTPException(
            status_code=400, detail="perusahaan belum terdaftar")
    return purchaseorders


@app.get("/purchaseorders/{purchaseorder_id}", response_model=schemas.PurchaseOrderDetailResponse)
def get_purchaseorders_by_id(company_id: int, purchaseorder_id=int, db: orm.Session = _fastapi.Depends(services.get_db)):
    purchaseorder_detail = services.get_purchaseorders_id(
        db=db, id_company=company_id, id_purchaseorder=purchaseorder_id)
    if purchaseorder_detail == 'companynotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="perusahaan belum terdaftar")
    elif purchaseorder_detail == 'purchaseordernotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="PO belum terdaftar")
    print(purchaseorder_detail)
    return purchaseorder_detail


@app.post("/inbounds/", response_model=List[schemas.PurchaseOrderDetailBase])
def get_inbounds(bound: schemas.BoundCreate, db: orm.Session = _fastapi.Depends(services.get_db)):
    if not bound.products:
        raise _fastapi.HTTPException(
            status_code=400, detail="List Product tidak boleh kosong")
    purchaseorder_detail = services.get_inbounds(db=db, bound=bound)
    if purchaseorder_detail == 'companynotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="perusahaan belum terdaftar")
    elif purchaseorder_detail == 'purchaseordernotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="PO belum terdaftar")
    elif purchaseorder_detail == 'productsinvalid':
        raise _fastapi.HTTPException(
            status_code=400, detail="Product tidak sesuai, mohon periksa kembali list barang PO anda")
    return purchaseorder_detail

@app.post("/outbounds/", response_model=List[schemas.PurchaseOrderDetailBase])
def get_outbounds(bound: schemas.BoundCreate, db: orm.Session = _fastapi.Depends(services.get_db)):
    if not bound.products:
        raise _fastapi.HTTPException(
            status_code=400, detail="List Product tidak boleh kosong")
    purchaseorder_detail = services.get_outbounds(db=db, bound=bound)
    if purchaseorder_detail == 'companynotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="perusahaan belum terdaftar")
    elif purchaseorder_detail == 'purchaseordernotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="PO belum terdaftar")
    elif purchaseorder_detail == 'productsinvalid':
        raise _fastapi.HTTPException(
            status_code=400, detail="Product tidak sesuai, mohon periksa kembali list barang PO anda")
    return purchaseorder_detail


@app.get("/low-stock", response_model=List[schemas.ProductBase])
def get_low_stock(company_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    lowstock = services.get_low_stock(id=company_id, db=db)
    if lowstock=='companynotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="perusahaan belum terdaftar")
    return lowstock

@app.get("/no-stock", response_model=List[schemas.ProductBase])
def get_no_stock(company_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
    nostock = services.get_no_stock(id=company_id, db=db)
    if nostock=='companynotfound':
        raise _fastapi.HTTPException(
            status_code=400, detail="perusahaan belum terdaftar")
    return nostock

# @app.get("/discontinued", response_model=List[schemas.ProductBase])
# def get_discontinued(company_id: int, db: orm.Session = _fastapi.Depends(services.get_db)):
#     nostock = services.get_discontinued(id=company_id, db=db)
#     if nostock=='companynotfound':
#         raise _fastapi.HTTPException(
#             status_code=400, detail="perusahaan belum terdaftar")
#     return nostock