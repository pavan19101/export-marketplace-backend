from sqlalchemy.orm import Session
from .database.db import SessionLocal, Base, engine
from .models import models
from .auth.auth_handler import get_password_hash

def seed_db():
    db = SessionLocal()
    
    # Check if we already have clients
    if db.query(models.Client).count() > 0:
        print("Database already seeded")
        db.close()
        return

    # 1. Seed Clients
    clients = [
        models.Client(
            name="John Doe", 
            email="john@example.com", 
            phone="1234567890", 
            password_hash=get_password_hash("password123"),
            address="123 Main St",
            country="USA"
        ),
        models.Client(
            name="Alice Smith", 
            email="alice@example.com", 
            phone="0987654321", 
            password_hash=get_password_hash("password123"),
            address="456 Elm St",
            country="Canada"
        )
    ]
    db.add_all(clients)
    db.commit()

    # 2. Seed Dealers
    dealers = [
        models.Dealer(
            name="Ramesh Exports",
            business_name="Ramesh & Co Export",
            email="ramesh@exports.com",
            phone="9988776655",
            category="Spices",
            rating=4.5
        ),
        models.Dealer(
            name="Global Trade Co",
            business_name="Global Trade Solutions",
            email="global@trade.com",
            phone="5544332211",
            category="Electronics",
            rating=4.8
        )
    ]
    db.add_all(dealers)
    db.commit()

    # 3. Seed Products
    products = [
        models.Product(
            name="Basmati Rice",
            description="Premium quality long grain rice",
            price=50.0,
            dealer_id=1,
            stock_quantity=1000,
            category="Food",
            port_details="Kolkata Port"
        ),
        models.Product(
            name="Raw Cotton",
            description="Organic raw cotton bales",
            price=200.0,
            dealer_id=1,
            stock_quantity=500,
            category="Textile",
            port_details="Mumbai Port"
        ),
        models.Product(
            name="Smartphone Galaxy X",
            description="Latest high-end smartphone",
            price=800.0,
            dealer_id=2,
            stock_quantity=50,
            category="Electronics",
            port_details="Delhi Air Cargo"
        )
    ]
    db.add_all(products)
    db.commit()

    # 4. Seed Stock
    for product in products:
        stock = models.Stock(
            product_id=product.id,
            available_quantity=product.stock_quantity
        )
        db.add(stock)
    db.commit()

    # 5. Seed Delivery Agents
    agents = [
        models.DeliveryAgent(
            name="Ravi Kumar",
            phone="1122334455",
            vehicle_number="KA-01-AB-1234",
            current_location="Bangalore",
            status=models.AgentStatus.AVAILABLE
        ),
        models.DeliveryAgent(
            name="Suresh Transport",
            phone="5566778899",
            vehicle_number="MH-02-CD-5678",
            current_location="Mumbai",
            status=models.AgentStatus.AVAILABLE
        )
    ]
    db.add_all(agents)
    db.commit()

    # 6. Seed a sample order
    client = clients[0]
    dealer = dealers[0]
    product = products[0]
    
    order = models.Order(
        client_id=client.id,
        dealer_id=dealer.id,
        product_id=product.id,
        delivery_agent_id=agents[0].id,
        quantity=2,
        total_price=product.price * 2,
        status=models.OrderStatus.PENDING,
        tracking_id="SAMPLE-TRACKING-123"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Add tracking history for the sample order
    tracking = models.Tracking(
        tracking_id="SAMPLE-TRACKING-123",
        order_id=order.id,
        status="Order Placed",
        location="Dealer Warehouse"
    )
    db.add(tracking)
    db.commit()

    print("Database seeded with sample data including orders")
    db.close()
