from fastapi import FastAPI
from datetime import datetime
import zoneinfo 
from models import Customer, Transaction, Invoice, CreateCustomer

app = FastAPI()

@app.get("/") # Decorator que define una ruta para el método GET
async def root(): # Método que se ejecuta cuando se accede a la ruta "/"
    return {"message": "Hello World"} # Retorna un diccionario con un mensaje



country_timezones = {
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "PE": "America/Lima",
}

format_codes = {
    "24" : "%H:%M:%S",
    "12" : "%I:%M:%S %p"
}

@app.get("/time/{iso_code}") # Decorator que define una ruta para el método GET con un parámetro en la URL 
async def time(iso_code: str): # Método que se ejecuta cuando se accede a la ruta "/time/{iso_code}"
    iso = iso_code.upper() # Convierte el código ISO a mayúsculas
    timezone_str = country_timezones.get(iso) # Obtiene la zona horaria del país
    tz = zoneinfo.ZoneInfo(timezone_str) # Crea un objeto de la clase ZoneInfo con la zona horaria
    return {"time": datetime.now(tz)} # Retorna un diccionario con la hora actual en la zona horaria del país


@app.get("/date/{iso_code}/{format_code}") # Decorator que define una ruta para el método GET con dos parámetros en la URL
async def date(iso_code: str, format_code: str): # Método que se ejecuta cuando se accede a la ruta "/date/{iso_code}/{format_code}"
    iso = iso_code.upper() # Convierte el código ISO a mayúsculas
    timezone_str = country_timezones.get(iso) # Obtiene la zona horaria del país
    tz = zoneinfo.ZoneInfo(timezone_str) # Crea un objeto de la clase ZoneInfo con la zona horaria
    format_code_srt = format_codes.get(format_code, "24") # Obtiene el formato de la fecha
    return {"date": datetime.now(tz).strftime(format_code_srt)} # Retorna un diccionario con la fecha actual en la zona horaria del país y el formato especificado


db_customer: list[Customer] = [] # Variable global para almacenar el ID actual

@app.post("/customers" , response_model=Customer) # Decorator que define una ruta para el método POST con un modelo de respuesta 
async def create_customer(customer_data: CreateCustomer): # Método que se ejecuta cuando se envía una solicitud POST a la ruta "/customers"
    customer = Customer.model_validate(customer_data.model_dump()) # Valida los datos del cliente y los convierte en un objeto de la clase Customer
    customer.id = len(db_customer)
    db_customer.append(customer)# Asigna un nuevo ID al cliente
    return customer # Retorna los datos del cliente recibidos en la solicitud

@app.get("/customers",response_model=list[Customer])
async def list_customers():
    return db_customer

@app.get("/customers/{customer_id}")# Decorator que define una ruta para el método GET con un parámetro en la URL y un modelo de respuesta
async def get_customer(customer_id: int): # Método que se ejecuta cuando se accede a la ruta "/customers/{customer_id}"
    for i in db_customer:
        if i.id == customer_id:
            return i

@app.post("/transactions") # Decorator que define una ruta para el método POST
async def create_transaction(transaction_data: Transaction): # Método que se ejecuta cuando se envía una solicitud POST a la ruta "/transactions"
    return transaction_data # Retorna los datos del cliente recibidos en la solicitud

@app.post("/invoices") # Decorator que define una ruta para el método POST
async def create_invoice(invoice_data: Invoice): # Método que se ejecuta cuando se envía una solicitud POST a la ruta "/invoices"
    return create_invoice # Retorna los datos del cliente recibidos en la solicitud