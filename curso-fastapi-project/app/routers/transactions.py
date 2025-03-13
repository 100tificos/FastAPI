from fastapi import APIRouter, HTTPException, status
from models import Transaction
from db import SessionDep
from sqlmodel import select


router = APIRouter()

@router.post("/transactions") 
async def create_transaction(transaction_data: Transaction, session:SessionDep): 
    return transaction_data 

async def list_transactions(session:SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions