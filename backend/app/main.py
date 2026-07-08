from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, crud, auth, database

app = FastAPI(title="MSME Decision Support API")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Auth routes ----------
@app.post("/register", response_model=schemas.UserRead)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ---------- Factory data routes ----------
@app.post("/factory-data", response_model=schemas.FactoryDataRead)
def create_factory_data(data: schemas.FactoryDataCreate, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.create_factory_data(db=db, data=data)

@app.get("/factory-data", response_model=list[schemas.FactoryDataRead])
def read_factory_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(auth.get_current_user)):
    return crud.get_factory_data(db=db, skip=skip, limit=limit)
