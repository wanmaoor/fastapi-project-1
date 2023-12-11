from fastapi import FastAPI, Depends
from dependencies import get_query_token
from routers import items
import uvicorn

app = FastAPI(
    dependencies=[Depends(get_query_token)]
)

app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Application"}
print(f'current name: {__name__}')
if __name__ == '__main__':
    print('start server')
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True, reload_dirs='*')
