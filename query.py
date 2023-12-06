from main import app

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get('/items')
async def read_item(skip: int = 0, limit: int = 10):
    """
    query 参数默认就在函数的参数拿到了
    """
    return fake_items_db[skip: skip + limit]
