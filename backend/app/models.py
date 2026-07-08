from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship to factory records
    records = relationship("FactoryData", back_populates="owner", cascade="all, delete-orphan")

class FactoryData(Base):
    __tablename__ = "factory_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Store date as string in YYYY-MM-DD format for SQLite ease of query and pandas alignment
    date = Column(String, index=True, nullable=False)
    
    sales = Column(Float, nullable=False)
    production = Column(Float, nullable=False)
    electricity_bill = Column(Float, nullable=False)
    raw_material_cost = Column(Float, nullable=False)
    salary = Column(Float, nullable=False)
    inventory = Column(Float, nullable=False)
    machine_running_hours = Column(Float, nullable=False)
    machine_downtime = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)

    owner = relationship("User", back_populates="records")
