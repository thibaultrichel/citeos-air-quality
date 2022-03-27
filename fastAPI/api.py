from fastapi import FastAPI
from get_predictions import getPredictions

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "test"}

async def pred():
