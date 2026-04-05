from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database.db import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class AgentStatus(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password_hash = Column(String)
    address = Column(String)
    country = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="client")
    ratings = relationship("Rating", back_populates="client")
    tickets = relationship("SupportTicket", back_populates="client")

class Dealer(Base):
    __tablename__ = "dealers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    business_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    category = Column(String)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="dealer")
    orders = relationship("Order", back_populates="dealer")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    stock_quantity = Column(Integer)
    category = Column(String)
    port_details = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dealer = relationship("Dealer", back_populates="products")
    orders = relationship("Order", back_populates="product")
    stock = relationship("Stock", back_populates="product", uselist=False)
    ratings = relationship("Rating", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    delivery_agent_id = Column(Integer, ForeignKey("delivery_agents.id"), nullable=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    tracking_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="orders")
    dealer = relationship("Dealer", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    delivery_agent = relationship("DeliveryAgent", back_populates="orders")
    tracking_history = relationship("Tracking", back_populates="order")

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    available_quantity = Column(Integer)
    reserved_quantity = Column(Integer, default=0)
    sold_quantity = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product = relationship("Product", back_populates="stock")

class DeliveryAgent(Base):
    __tablename__ = "delivery_agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    vehicle_number = Column(String)
    current_location = Column(String)
    status = Column(Enum(AgentStatus), default=AgentStatus.AVAILABLE)

    orders = relationship("Order", back_populates="delivery_agent")

class Tracking(Base):
    __tablename__ = "tracking"
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    status = Column(String)
    location = Column(String)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order = relationship("Order", back_populates="tracking_history")

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer) # 1-5
    review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    subject = Column(String)
    description = Column(Text)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="tickets")

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    code = Column(String)
    expires_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
