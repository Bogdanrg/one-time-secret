from fastapi import FastAPI
from config.database import db


app = FastAPI(
    title="Secret!"
)


@app.get('/')
def hello():
    return "hello"
