from fastapi import FastAPI

from .routers import validate

app = FastAPI()
app.include_router(validate.router)

@app.get("/")
async def root():
    return {"message": "welcome to the pepserver"}