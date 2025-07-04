from fastapi import FastAPI
from app.routes import transactions
from app.db import models
from app.db.database import engine
from app.routes import auth_routes, account_routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin ftbs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tables 
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the Ledger Banking API"}

# Register routes
app.include_router(transactions.router)
app.include_router(auth_routes.router)
app.include_router(account_routes.router)

# uvicorn app.main:app --reload