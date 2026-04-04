from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.db import engine, Base
from .routes import auth_routes, marketplace_routes, ops_routes, support_routes
from .seed import seed_db

# Create all database tables
Base.metadata.create_all(bind=engine)

# Seed the database if empty
seed_db()

app = FastAPI(
    title="Export Marketplace Backend",
    description="Production-ready FastAPI backend for an Export Marketplace platform.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth_routes.router)
app.include_router(marketplace_routes.router)
app.include_router(ops_routes.router)
app.include_router(support_routes.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the Export Marketplace API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
