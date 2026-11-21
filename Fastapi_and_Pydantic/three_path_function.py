from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()


# create the helper function to load the data

def load_data():
    with open("Fastapi_and_Pydantic/trainers_db.json") as f:
        data = json.load(f)

    return data



@app.get('/')
def hello():
    return {"message": "trainers info api"}


@app.get('/info')
def info():
    return {'message': 'functional api to manage trainers info'}

# endpoint to see all the info

@app.get('/view')
def view():
    data = load_data()
    return data


# endpoint to see the info of specific user

@app.get('/view/{trainer_id}')   # {} -> path variable
def view_id_info(trainer_id: str = Path(..., description= "id of the trainer", example= "105")):
    data = load_data()

    id = "user_" + str(trainer_id)

    if id in data:
        return data[id]
    raise HTTPException(status_code= 404, detail= "trainer is not in the database")


# Query Parameters

# will have 2 things -> sort by level, name..... order -> asc or desc

@app.get('/sort')
def sort_trainers(sort_by: str = Query(..., description= 'sort on the basis of the trainer name or level'), order: str = Query('asc', description= 'sort in ascending or descending order')):

    valid_fields = ['name', 'level']

    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail= f'invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code= 400, detail= f'invalid field select between asc or desc')

    data = load_data()

    sort_order = True if order == 'desc' else False
    
    # sorting
    sorted_data = sorted(data.values(),
                         key = lambda x: x.get(sort_by, 0),
                         reverse= sort_order)

    return sorted_data
