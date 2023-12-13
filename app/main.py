from fastapi import FastAPI, Depends
from .dependencies import get_query_token
from .routers import items
from .notification import main
app = FastAPI(
    dependencies=[Depends(get_query_token)]
)

app.include_router(items.router)
app.include_router(main.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Application"}
print(f'current name: {__name__}')

