import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Path, Body, status, Form, UploadFile, File, HTTPException
from typing import Annotated
from enum import Enum
from fastapi.encoders import jsonable_encoder


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
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.post("/items", status_code=status.HTTP_201_CREATED, response_description="创建新的项")
async def create_item(item: Item):
    """
    Create an item with all the information
    - **name** - the name of the item
    - **description** - the description of the item
    - **price** - the price of the item
    - **tax** - the tax of the item
    - **tag** - the tag of the item
    :param item:
    :return:
    """
    return {"status": "success", **item.model_dump()}


items = {"foo": "the foo wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"item": items.get(item_id)}


db = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.patch("/items/{item_id}", response_model=Item)
async def patch_item(item_id: str, item: Item):
    # 获取原始数据
    stored_item_data = db[item_id]
    print(f'stored_item_data: {stored_item_data}')
    stored_item_model = Item(**stored_item_data)
    print(f"stored_item_model: {stored_item_model}")
    # 拿到客户端的数据，同时不要默认值数据
    update_data = item.dict(exclude_unset=True)
    print(f'update_data: {update_data}')
    # 将原有值和新数据进行合并
    updated_item = stored_item_model.copy(update=update_data)
    print(f"updated_item: {updated_item}")
    # 将新数据转换为json格式存储
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

fake_db = {}


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
    fake_db[item_id] = jsonable_encoder(item)
    print(f'fake_db: {fake_db}')
    return results


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password": password}


@app.post("/files/", tags=['文件上传'])
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile", tags=['文件上传'])
async def create_upload_file(file: UploadFile):
    return {"file_name": file.filename}


if __name__ == '__main__':
    print('start server')
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, reload_dirs='*')
