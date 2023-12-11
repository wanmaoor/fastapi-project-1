from app.other.main import app
from fastapi import Query, Path
from typing import Annotated
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get('/item')
async def read_item(skip: int = 0, limit: int = 10):
    """
    query 参数默认就在函数的参数拿到了
    """
    return fake_items_db[skip: skip + limit]


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=5)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def get_items_by_id(
        item_id: Annotated[int, Path(title="The ID of the item to get")],
        q: Annotated[str | None, Query(alias="item-query")] = None
):

    results = {"item_id": item_id}
    if q:
        results.update({"q": q})

    return results
