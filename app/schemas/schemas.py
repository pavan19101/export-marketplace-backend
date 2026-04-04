from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from ..models.models import OrderStatus, AgentStatus, TicketPriority, TicketStatus

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    address: str
    country: str

class ClientLogin(BaseModel):
    email: EmailStr
    password: str

class ClientOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: str
    country: str
    created_at: datetime
    class Config:
        from_attributes = True

class DealerOut(BaseModel):
    id: int
    name: str
    business_name: str
    email: str
    phone: str
    category: str
    rating: float
    created_at: datetime
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    dealer_id: int
    stock_quantity: int
    category: str
    port_details: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None
    port_details: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    dealer_id: int
    stock_quantity: int
    category: str
    port_details: str
    created_at: datetime
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    dealer_id: int
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    client_id: int
    dealer_id: int
    product_id: int
    delivery_agent_id: Optional[int] = None
    quantity: int
    total_price: float
    status: OrderStatus
    tracking_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class TrackingOut(BaseModel):
    id: int
    tracking_id: str
    order_id: int
    status: str
    location: str
    updated_at: datetime
    class Config:
        from_attributes = True

class DeliveryAgentOut(BaseModel):
    id: int
    name: str
    phone: str
    vehicle_number: str
    current_location: str
    status: AgentStatus
    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    review: str

class RatingOut(BaseModel):
    id: int
    client_id: int
    product_id: int
    rating: int
    review: str
    created_at: datetime
    class Config:
        from_attributes = True

class SupportTicketCreate(BaseModel):
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM

class SupportTicketOut(BaseModel):
    id: int
    client_id: int
    subject: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    class Config:
        from_attributes = True
