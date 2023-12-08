import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Path, Body
from typing import Annotated
from enum import Enum


class ModelName(int, Enum):
    alexnet = 1
    resnet = 2
    lenet = 3


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hell"}


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


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.post("/items")
async def create_item(item: Item):
    return {"status": "success", **item.model_dump()}


# query, path, request body 混合传参
@app.put("/item/{item_id}")
async def update_item(
        importance: Annotated[int, Body()],
        item_id: Annotated[
            int, Path(title="The ID of the item to update", description="The ID of the item to", ge=0, le=1000)],
        q: str | None = None,
        item: Item | None = None,
        user: User | None = None,
):
    results = {"item_id": item_id}
    if q is not None:
        results.update({"q": q})
    if item is not None:
        results.update({"item": item})
    if user is not None:
        results.update({"user": user})
    if importance is not None:
        results.update({"importance": importance})

    return results


if __name__ == '__main__':
    print('start server')
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, reload_dirs='*')
