import database
import models
from sqlalchemy.orm import Session
import schemas
from datetime import datetime


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.owner_name == name).first()

def get_company_by_email(db: Session, email: str):
    return db.query(models.Company).filter(models.Company.owner_email == email).first()

def create_company(db: Session, company: schemas.CompanyCreate ):
    fake_hashed_password = company.owner_password + "thisisnotsecured"
    db_company = models.Company(
        created_at=datetime.now(),
        owner_name=company.owner_name,
        name=company.name,
        owner_email=company.owner_email,
        owner_password=company.owner_password
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    db_company = schemas.Company(
        id=db_company.id,
        created_at=db_company.created_at,
        owner_name=db_company.owner_name,
        name=db_company.name,
        owner_email=db_company.owner_email,
    )
    return db_company