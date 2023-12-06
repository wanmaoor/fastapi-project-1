from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(nam: str):
    print('name: ', nam)
    return {"message": f"Hello {nam}"}
