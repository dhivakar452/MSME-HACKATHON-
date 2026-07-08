from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# --- User CRUD ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Factory Data CRUD ---
def get_factory_data(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.FactoryData]:
    return (
        db.query(models.FactoryData)
        .filter(models.FactoryData.user_id == user_id)
        .order_by(models.FactoryData.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_factory_data_by_date(db: Session, user_id: int, date: str) -> Optional[models.FactoryData]:
    return (
        db.query(models.FactoryData)
        .filter(models.FactoryData.user_id == user_id, models.FactoryData.date == date)
        .first()
    )

def get_latest_factory_data(db: Session, user_id: int) -> Optional[models.FactoryData]:
    return (
        db.query(models.FactoryData)
        .filter(models.FactoryData.user_id == user_id)
        .order_by(models.FactoryData.date.desc())
        .first()
    )

def create_factory_data(db: Session, data: schemas.FactoryDataCreate, user_id: int) -> models.FactoryData:
    # Check if entry for date already exists, update it if it does
    existing_record = get_factory_data_by_date(db, user_id, data.date)
    if existing_record:
        for key, value in data.model_dump().items():
            setattr(existing_record, key, value)
        db.commit()
        db.refresh(existing_record)
        return existing_record

    db_data = models.FactoryData(**data.model_dump(), user_id=user_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def bulk_create_factory_data(db: Session, data_list: List[schemas.FactoryDataCreate], user_id: int) -> List[models.FactoryData]:
    records = []
    for data in data_list:
        existing_record = get_factory_data_by_date(db, user_id, data.date)
        if existing_record:
            for key, value in data.model_dump().items():
                setattr(existing_record, key, value)
            records.append(existing_record)
        else:
            db_record = models.FactoryData(**data.model_dump(), user_id=user_id)
            db.add(db_record)
            records.append(db_record)
    db.commit()
    return records
