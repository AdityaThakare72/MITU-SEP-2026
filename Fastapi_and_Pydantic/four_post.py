from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated, List

from fastapi.responses import JSONResponse

import json

app = FastAPI()



# helper function to load the data
def load_data():
    with open('FastAPI/trainers_db.json', 'r') as f:
        data = json.load(f)

    return data

# helper function to save/add data
def save_data(data):
    with open('FastAPI/trainers_db.json', 'w') as f:
        json.dump(data, f, indent= 4)  # dumping into f

# pydantic model for validating the data

class Trainer(BaseModel):

    id: Annotated[str, Field(..., description= "id of the trainer", examples= ['user_101'])]

    # The ... means this field is strictly REQUIRED. It has no default value, and the user cannot skip it.
    # NOTE: Because you are using modern Pydantic with Annotated, the framework has actually become much smarter. In the newest versions, if you leave the first argument completely empty, Pydantic automatically assumes it is required!

    name: Annotated[str, Field(..., max_length= 50, description= "name of the trainer less than 50 char")]

    region: Annotated[str, Field(..., max_length= 15, description= "region of the trainer")]

    level: Annotated[int, Field(..., ge= 0, lt = 101, description= "level of the trainer in beetween 0 to 101")]

    pokedex: Annotated[List[str], Field(...,max_length= 10, description= "pokemons owned by the trainer, max can be 10")]


# home endpoint
@app.get('/')
def hello():
    return {'message': "pokemon trainers info API"}


@app.get('/about')
def info():
    return {'message': 'functional api to manage the trainers info'}


# post endpoint for creating a new trainer
@app.post('/create')
def create_trainer(trainer_info: Trainer):   # here the data will of json type in the variable trainer_info and the datatype will be of our pydantic model Trainer

    # laod existin data and check if the trainer already exists
    data = load_data()

    if trainer_info.id in data:
        raise HTTPException(status_code= 400, detail= "trainer id already exists")


    # new trainer add in database
    data[trainer_info.id] = trainer_info.model_dump(exclude= ['id'])  # model_dump converts the pydantic object to dict.
    # also excluding the id because of the format of the data we have ==> so we will have a dict called data with keys as id and then values as the dict of remaining data

    # save the above dict as the json file
    save_data(data)

    return JSONResponse(status_code= 201, content = {'message': "trainer created successfully"})