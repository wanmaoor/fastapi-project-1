from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from .dependencies import get_query_token
from .routers import items
from .notification import main

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "通知",
        "description": "背景任务相关",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="ChimichangApp API helps",
    version="0.0.1",
    terms_of_service="https://www.google.com/policies",
    contact={
        "name": "wanmao",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    dependencies=[Depends(get_query_token)],
    openapi_tags=tags_metadata
)

app.include_router(items.router)
app.include_router(main.router)
app.mount("/", StaticFiles(directory="static"), name="")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Application"}


print(f'current name: {__name__}')
