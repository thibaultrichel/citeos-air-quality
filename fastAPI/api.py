from fastapi import FastAPI
from get_predictions import getPredictions
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "test"}


@app.get("/pred")
async def pred():
    value = getPredictions()
    return {"pred": value}
