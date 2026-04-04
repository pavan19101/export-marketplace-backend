from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import random
from ..database.db import get_db
from ..models import models
from ..schemas import schemas
from ..auth.auth_bearer import get_current_user

router = APIRouter(tags=["Operations"])

@router.post("/orders", response_model=schemas.OrderOut, description="Create a new order, reduce stock, assign a delivery agent, and generate a tracking ID.")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    stock = db.query(models.Stock).filter(models.Stock.product_id == order.product_id).first()
    if not stock or stock.available_quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    total_price = product.price * order.quantity
    tracking_id = str(uuid.uuid4())[:8].upper()
    
    # Assign delivery agent if available
    agent = db.query(models.DeliveryAgent).filter(models.DeliveryAgent.status == models.AgentStatus.AVAILABLE).first()
    agent_id = None
    if agent:
        agent.status = models.AgentStatus.BUSY
        agent_id = agent.id
    
    new_order = models.Order(
        client_id=current_user.id,
        dealer_id=order.dealer_id,
        product_id=order.product_id,
        delivery_agent_id=agent_id,
        quantity=order.quantity,
        total_price=total_price,
        status=models.OrderStatus.PENDING,
        tracking_id=tracking_id
    )
    db.add(new_order)
    
    # Update stock
    stock.available_quantity -= order.quantity
    stock.reserved_quantity += order.quantity
    
    db.commit()
    db.refresh(new_order)
    
    # Create tracking record
    new_tracking = models.Tracking(
        tracking_id=tracking_id,
        order_id=new_order.id,
        status="Order Placed",
        location="Dealer Warehouse"
    )
    db.add(new_tracking)
    db.commit()
    
    return new_order

@router.get("/orders", response_model=List[schemas.OrderOut], description="Get a list of all orders for the current user.")
def list_orders(db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    return db.query(models.Order).filter(models.Order.client_id == current_user.id).all()

@router.get("/orders/{id}", response_model=schemas.OrderOut, description="Get details of a specific order.")
def get_order(id: int, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == id, models.Order.client_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/tracking/{tracking_id}", response_model=List[schemas.TrackingOut], description="Get the tracking history for a given tracking ID.")
def get_tracking(tracking_id: str, db: Session = Depends(get_db)):
    history = db.query(models.Tracking).filter(models.Tracking.tracking_id == tracking_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return history

@router.get("/delivery-agents", response_model=List[schemas.DeliveryAgentOut], description="Get a list of all delivery agents.")
def list_agents(db: Session = Depends(get_db)):
    return db.query(models.DeliveryAgent).all()
