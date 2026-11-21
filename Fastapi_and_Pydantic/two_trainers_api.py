from fastapi import FastAPI
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
def view_id_info(trainer_id: str):
    data = load_data()

    id = "user_" + str(trainer_id)

    return data.get(id)  # data['id']