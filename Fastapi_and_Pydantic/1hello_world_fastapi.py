from fastapi import FastAPI

app = FastAPI()

# follow ->
# conda activate genai
# cd <path to the project>
# uvicorn Fastapi_and_Pydantic.1hello_world_fastapi:app --reload

@app.get('/')   # endpoint...home
def greet():
    return 'hello world'

@app.get('/other')   # endpoint...home
def other():
    return 'this is the other page'

@app.get('/info')
def info():
    return {'name': 'Aditya Thakare', 'des': 'Data Scientist'}
# uvicorn Fastapi_and_Pydantic.1hello_world_fastapi:app --reload
# uvicorn <file path without .py extention>:app --reload
# for path use . instead of /