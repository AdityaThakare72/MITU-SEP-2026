from fastapi import FastAPI
import json

app = FastAPI()


# create the helper function to load the data

def load_data():
    with open("Fastapi_and_Pydantic/employees_db.json") as f:
        data = json.load(f)

    return data



@app.get('/')
def hello():
    return {"message": "company employees info API"}


# endpoint to see all the info

@app.get('/view')
def view():
    data = load_data()
    return data