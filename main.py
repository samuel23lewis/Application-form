from fastapi import FastAPI, Form
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="application_db"
    )

class Application(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

# Endpoint to handle the form submission
@app.post("/submit/")
async def submit_application(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_number: str = Form(...)
):
    # Get a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the form data into the database
    cursor.execute(
        "INSERT INTO applications (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
        (first_name, last_name, phone_number)
    )
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return {"message": f"Dear {first_name} {last_name}, your application has been submitted"}
