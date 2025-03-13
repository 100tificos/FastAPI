from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    age: int = Field(default=None)
    email: EmailStr = Field(default=None)
    
class CreateCustomer(CustomerBase):
    pass 

class UpdateCustomer(CustomerBase):
    pass    

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    

class TransactionBase(SQLModel):
    amount: float = Field(default=None)
    description: str = Field(default=None)
   

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id")
    customer= Relationship(back_populates="transactions")



class Invoice(BaseModel):
    id: int = Field(default=None, primary_key=True)
    customer: Customer = Field(default=None)
    transactions: list[Transaction] = Field(default=None)
    total: int = Field(default=None)
    
    @property
    def ammount_total(self):
        return sum([transaction.amount for transaction in self.transactions])