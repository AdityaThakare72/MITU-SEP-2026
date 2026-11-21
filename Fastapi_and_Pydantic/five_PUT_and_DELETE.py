"""For update we use -> PUT

So we are going to have a put method to update/change the info of a trainer
Someone can change one or more/ any info in the existing one
That is the reason why we will need another pydantic model for PUT because the previous one had all the fields as required. And for this one we will need to make them optional
""";

# will take the same code as well of post

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Annotated, List, Optional

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


# ------------ UPDATE ----------------

class TrainerUpdate(BaseModel):

    id: Annotated[Optional[str], Field(default=None)]
    name: Annotated[Optional[str], Field(default=None)]
    region: Annotated[Optional[str], Field(default=None)]
    level: Annotated[Optional[int], Field(default=None, ge = 0, lt = 101)]
    pokedex: Annotated[Optional[List[str]], Field(default=None)]



@app.put('/edit/{trainer_id}')
def update_trainer(trainer_id: str, trainer_update_content: TrainerUpdate):

    # above trainer_update_content variable is the request body having the info regardinbg the changes

    # laod the existing data
    data = load_data()

    # check if the trainer id there in the data
    if trainer_id not in data:
        raise HTTPException(status_code= 400, detail= "wrong trainer id")
    

    # extract the info of that particular patient id
    existing_trainer_info = data[trainer_id]

    # convert the pydantic object into dict as well

    trainer_info_to_update = trainer_update_content.model_dump(exclude_unset = True) # will only have the fields which are required to be changed and not all of them

    # using for loop update
    for key, val in trainer_info_to_update.items():
        existing_trainer_info[key] = val

    data[trainer_id] = existing_trainer_info # will not work if there is some computed field is there

    # save the data
    save_data(data)


    return JSONResponse(status_code= 200, content= {'message': "trainer updated"})



# ----------- DELETE -------------

@app.delete("/delete/{trainer_id}")
def delete_trainer(trainer_id: str):

    data = load_data()

    if trainer_id not in data:
        raise HTTPException(status_code= 404, detail= "trainer id does not exist")
    
    del data[trainer_id]

    save_data(data)

    return JSONResponse(status_code= 200, content= {'message': "trainer deleted successfully"})