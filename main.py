import uvicorn
import query
from fastapi import FastAPI
from enum import Enum


class ModelName(int, Enum):
    alexnet = 1
    resnet = 2
    lenet = 3


app = FastAPI()


@app.get("/")
async def root():
    print('执行/')
    return {"message": "Hello"}


@app.get("/hello/{name}")
async def say_hello(name: int):
    return {"message-nae": name}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name)
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, 'message': 'Deep Learning FTW!'}

    if model_name.value == 2:
        return {"model_name": model_name, 'message': 'LeCNN all the images'}

    return {"model_name": model_name, "message": "Have some residuals"}


if __name__ == '__main__':
    print('start server')
    uvicorn.run('main:app', host='127.0.0.1', port=8888, reload=True)
