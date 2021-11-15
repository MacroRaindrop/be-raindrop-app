from sqlalchemy.sql.expression import update
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

def get_company_by_id(db: Session, id: int):
    return db.query(models.Company).filter(models.Company.id == id).first()

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
    db_company = schemas.CompanyBase(
        id=db_company.id,
        created_at=db_company.created_at,
        owner_name=db_company.owner_name,
        name=db_company.name,
        owner_email=db_company.owner_email,
        owner_password=db_company.owner_password
    )
    return db_company

def create_product(db: Session, product: schemas.ProductCreate ):
    db_product = models.Product(
        created_at=datetime.now(),
        id_company=product.id_company,
        name=product.name,
        minimum_stock=product.minimum_stock,
        image=product.image,
        unit=product.unit,
        description=product.description,
        quantity=product.quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db_product = schemas.ProductBase(
        id=db_product.id,
        created_at=db_product.created_at,
        id_company=db_product.id_company,
        name=db_product.name,
        minimum_stock=db_product.minimum_stock,
        image=db_product.image,
        unit=db_product.unit,
        description=db_product.description,
        quantity=db_product.quantity
    )
    return db_product

def get_products(db: Session, skip:int, limit:int):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id).first()

def get_products_by_user(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id_company == id).all()

def update_product(db: Session, product: schemas.ProductBase):
    db.execute(
        update(models.Product).
        where(models.Product.id == product.id).
        values(
            id_company=product.id_company,
            name=product.name,
            minimum_stock=product.minimum_stock,
            image=product.image,
            unit=product.unit,
            description=product.description,
            quantity=product.quantity
        )
    )
    db.commit()
    product =  db.query(models.Product).filter(models.Product.id == product.id).first()
    return product

def delete_product(db: Session, id: int):
    product =  db.query(models.Product).filter(models.Product.id == id).first()
    db.delete(product)
    db.commit()
    return product

def get_pics(db: Session, id:int):
    return db.query(models.Staff).filter(models.Staff.id_company == id).all()
    
def get_owner_name(db: Session, id: int):
    return db.query(models.Company).filter(models.Company.id == id).first()

def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(
        created_at=datetime.now(),
        id_company=staff.id_company,
        name=staff.name,
        email=staff.email,
        password=staff.password,
        role=staff.role
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    db_staff = schemas.StaffBase(
        id=db_staff.id,
        created_at=db_staff.created_at,
        id_company=db_staff.id_company,
        name=db_staff.name,
        email=db_staff.email,
        password=db_staff.password,
        role=db_staff.role
    )
    return db_staff