from fastapi import FastAPI
import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware

import services
services.create_database()

import sqlalchemy.orm as orm

import schemas


app = _fastapi.FastAPI()

@app.post("/companies", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: orm.Session=_fastapi.Depends(services.get_db)):
    db_name= services.get_company_by_name(db=db, name=company.name)
    db_email= services.get_company_by_email(db=db, email=company.owner_email)
    if db_name:
        raise _fastapi.HTTPException(status_code=400, detail="the company name is exist")
    elif db_email:
        raise _fastapi.HTTPException(status_code=400, detail="the email is in use")
    return services.create_company(db=db, company=company)

@app.post("/login", response_model=schemas.Company)
def login_company(company: schemas.CompanyLogin, db: orm.Session=_fastapi.Depends(services.get_db)):
    db_company = services.get_company_by_email(db=db, email=company.owner_email)
    if not db_company:
        raise _fastapi.HTTPException(status_code=400, detail="the company is not found")
    if db_company.owner_password!=company.owner_password:
        raise _fastapi.HTTPException(status_code=401, detail="the password is incorrect")
    db_company = schemas.Company(
        id=db_company.id,
        created_at=db_company.created_at,
        owner_name=db_company.owner_name,
        name=db_company.name,
        owner_email=db_company.owner_email,
    )
    return db_company