from fastapi import FastAPI
from models import Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
from .routers import customer

app = FastAPI(lifespan=create_all_tables) # Crea una instancia de la clase FastAPI 
app.include_router(customer.router)


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return create_invoice