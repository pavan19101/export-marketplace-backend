from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.db import get_db
from ..models import models
from ..schemas import schemas
from ..auth.auth_bearer import get_current_user

router = APIRouter(tags=["Marketplace"])

# Clients
@router.get("/clients/me", response_model=schemas.ClientOut, description="Get details of the currently authenticated client.")
def read_current_client(current_user: models.Client = Depends(get_current_user)):
    return current_user

# Dealers
@router.get("/dealers", response_model=List[schemas.DealerOut], description="Get a list of all exporters/dealers.")
def list_dealers(db: Session = Depends(get_db)):
    return db.query(models.Dealer).all()

@router.get("/dealers/{id}", response_model=schemas.DealerOut, description="Get details of a specific dealer.")
def get_dealer(id: int, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealer).filter(models.Dealer.id == id).first()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")
    return dealer

# Products
@router.get("/products", response_model=List[schemas.ProductOut], description="Get a list of all products in the marketplace.")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.get("/products/{id}", response_model=schemas.ProductOut, description="Get details of a specific product.")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=schemas.ProductOut, description="Add a new product to the marketplace.")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Check if dealer exists
    dealer = db.query(models.Dealer).filter(models.Dealer.id == product.dealer_id).first()
    if not dealer:
        raise HTTPException(status_code=400, detail="Dealer does not exist")
        
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Initialize stock
    db_stock = models.Stock(product_id=db_product.id, available_quantity=db_product.stock_quantity)
    db.add(db_stock)
    db.commit()
    
    return db_product

@router.put("/products/{id}", response_model=schemas.ProductOut, description="Update an existing product's details.")
def update_product(id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product
