from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Customer, CreateCustomer, UpdateCustomer
from db import SessionDep


router = APIRouter()


#create customer
@router.post("/customers" , response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers']) # Decorator que define una ruta para el método POST con un modelo de respuesta 
async def create_customer(customer_data: CreateCustomer, session:SessionDep, ): # Método que se ejecuta cuando se envía una solicitud POST a la ruta "/customers"
    customer = Customer.model_validate(customer_data.model_dump()) 
    session.add(customer) 
    session.commit() 
    session.refresh(customer)
    return customer 

#get list of customers
@router.get("/customers",response_model=list[Customer],status_code=status.HTTP_200_OK, tags=['Customers'])
async def list_customers(session:SessionDep):
    return session.exec(select(Customer)).all()
    
#get customer by id
@router.get("/customers/{customer_id}",status_code=status.HTTP_200_OK, tags=['Customers'])
async def read_customer(customer_id: int, session:SessionDep): 
    if  session.get(Customer, customer_id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return session.get(Customer, customer_id)

#delete customer by id
@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Customers'])
async def delete_customer(customer_id: int, session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return {"detail":"ok"}

#update customer by id
@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def update_customer(customer_id: int, customer_data: UpdateCustomer, session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db