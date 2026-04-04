from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.db import get_db
from ..models import models
from ..schemas import schemas
from ..auth.auth_bearer import get_current_user

router = APIRouter(tags=["Support & Ratings"])

@router.post("/ratings", response_model=schemas.RatingOut, description="Submit a rating and review for a product. Only allowed for products you have ordered.")
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    # Check if order exists for this user and product
    order = db.query(models.Order).filter(models.Order.client_id == current_user.id, models.Order.product_id == rating.product_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="You can only rate products you have ordered")
        
    db_rating = models.Rating(**rating.dict(), client_id=current_user.id)
    db.add(db_rating)
    
    # Update product dealer rating average
    product = db.query(models.Product).filter(models.Product.id == rating.product_id).first()
    dealer = db.query(models.Dealer).filter(models.Dealer.id == product.dealer_id).first()
    
    # Simple average logic
    all_ratings = db.query(models.Rating).join(models.Product).filter(models.Product.dealer_id == dealer.id).all()
    total_rating = sum([r.rating for r in all_ratings]) + rating.rating
    dealer.rating = total_rating / (len(all_ratings) + 1)
    
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/ratings/product/{product_id}", response_model=List[schemas.RatingOut], description="Get all ratings and reviews for a specific product.")
def get_product_ratings(product_id: int, db: Session = Depends(get_db)):
    return db.query(models.Rating).filter(models.Rating.product_id == product_id).all()

@router.post("/support/tickets", response_model=schemas.SupportTicketOut, description="Create a new support ticket.")
def create_ticket(ticket: schemas.SupportTicketCreate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    db_ticket = models.SupportTicket(**ticket.dict(), client_id=current_user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/support/tickets", response_model=List[schemas.SupportTicketOut], description="List all support tickets created by the current user.")
def list_tickets(db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    return db.query(models.SupportTicket).filter(models.SupportTicket.client_id == current_user.id).all()
