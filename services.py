from sqlalchemy.sql.expression import null, update
from sqlalchemy.sql.functions import mode
import database
import models
from sqlalchemy.orm import Session
import schemas
from datetime import datetime
from sqlalchemy import and_
from typing import List


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


def create_company(db: Session, company: schemas.CompanyCreate):
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


def create_product(db: Session, product: schemas.ProductCreate):
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


def get_products(db: Session, skip: int, limit: int):
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
    product = db.query(models.Product).filter(
        models.Product.id == product.id).first()
    return product


def delete_product(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    db.delete(product)
    db.commit()
    return product


def get_staff(db: Session, id: int):
    return db.query(models.Staff).filter(models.Staff.id_company == id).all()


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


def create_purchaseorder(db: Session, purchaseorder: schemas.PurchaseOrderCreate):
    purchaseorders = db.query(models.Purchaseorder).filter(
        models.Purchaseorder.id_company == purchaseorder.id_company).all()
    if not purchaseorders:
        id = 1
    else:
        id = purchaseorders[-1].id_purchaseorder + 1
    db_purchaseorder = models.Purchaseorder(
        created_at=datetime.now(),
        id_purchaseorder=id,
        id_company=purchaseorder.id_company,
        id_staff=purchaseorder.id_staff,
        supplier=purchaseorder.supplier,
        date=purchaseorder.date
    )
    db.add(db_purchaseorder)
    db.commit()
    db.refresh(db_purchaseorder)
    db_purchaseorder = schemas.PurchaseOrderBase(
        id=db_purchaseorder.id,
        created_at=db_purchaseorder.created_at,
        id_purchaseorder=db_purchaseorder.id_purchaseorder,
        id_company=db_purchaseorder.id_company,
        id_staff=db_purchaseorder.id_staff,
        supplier=db_purchaseorder.supplier,
        date=db_purchaseorder.date
    )
    purchaseorderdetails = []
    for i in range(len(purchaseorder.products)):
        purchaseorderdetail = models.PurchaseorderDetail(
            id_company=db_purchaseorder.id_company,
            id_purchaseorder=db_purchaseorder.id,
            id_product=purchaseorder.products[i].id_product,
            quantity=purchaseorder.products[i].quantity
        )
        purchaseorderdetails.append(purchaseorderdetail)
    db.add_all(purchaseorderdetails)
    db.commit()
    result = schemas.PurchaseOrderDetailResponse(
        id_purchaseorder=db_purchaseorder.id_purchaseorder,
        id_company=db_purchaseorder.id_company,
        id_staff=db_purchaseorder.id_staff,
        supplier=db_purchaseorder.supplier,
        date=db_purchaseorder.date,
        products=purchaseorder.products
    )
    return result


def get_purchaseorders(db: Session, id: int):
    return db.query(models.Purchaseorder).filter(models.Purchaseorder.id_company == id).all()


def get_purchaseorders_id(db: Session, id_company: int, id_purchaseorder: int):
    purchaseorders = db.query(models.Purchaseorder).filter(
        models.Purchaseorder.id_company == id_company).all()
    if not purchaseorders:
        return 'companynotfound'
    purchaseorder_detail = db.query(models.PurchaseorderDetail).filter(and_(
        models.PurchaseorderDetail.id_purchaseorder == id_purchaseorder, models.PurchaseorderDetail.id_company == id_company)).first()
    if not purchaseorder_detail:
        return 'purchaseordernotfound'
    return purchaseorder_detail


def get_inbounds(db: Session, inbound: schemas.InboundCreate):
    purchaseorders = db.query(models.Purchaseorder).filter(
        models.Purchaseorder.id_company == inbound.id_company).all()
    if not purchaseorders:
        return 'companynotfound'
    purchaseorder_detail = db.query(models.PurchaseorderDetail).filter(and_(
        models.PurchaseorderDetail.id_purchaseorder == inbound.id_purchaseorder, models.PurchaseorderDetail.id_company == inbound.id_company)).all()
    if not purchaseorder_detail:
        return 'purchaseordernotfound'
    for i in range(len(purchaseorder_detail)):
        if not purchaseorder_detail[i].id_product == inbound.products[i].id_product:
            return 'productsinvalid'
    # history = db.query(models.History)
    histories = []
    for i in range(len(inbound.products)):
        id_product = inbound.products[i].id_product
        quantity = inbound.products[i].quantity
        histories.append(
            models.History(
                created_at=datetime.now(),
                id_company=inbound.id_company,
                id_product=id_product,
                inbound=quantity,
                outbound=0,
                notes=inbound.notes
        ))
        db.execute(
            update(models.Product).
            where(models.Product.id == id_product).
            values(
                quantity=quantity
            )
        )
    db.add_all(histories)
    db.commit()
    return purchaseorder_detail
