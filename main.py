from typing import Annotated
from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from cryptocode import encrypt, decrypt
from config.settings import ENCODING
from config.database import db
from schemas import CreateSecretModel
from werkzeug.security import generate_password_hash, check_password_hash

app = FastAPI(
    title="Secret!"
)


@app.post('/generate', response_description="Generated secret key")
async def generate_secret_key(secret: CreateSecretModel = Body(...)):
    secret = jsonable_encoder(secret)
    secret['secret'] = encrypt(secret['secret'], ENCODING)
    secret['phrase'] = generate_password_hash(secret['phrase'])
    new_secret = await db["secrets"].insert_one(secret)
    created_secret = await db["secrets"].find_one({"_id": new_secret.inserted_id})
    secret_key = f"127.0.0.1:8000/secrets/{created_secret['_id']}"
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=secret_key)


@app.post('/secrets/{secret_key}', response_description="received secret, remember you can see it once, then it will "
                                                        "be deleted")
async def get_secret(secret_key: str, phrase: Annotated[str, Body()]):
    try:
        secret_dict = await db['secrets'].find_one({"_id": secret_key})
        if not check_password_hash(secret_dict['phrase'], phrase):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid secret phrase or secret key")
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This secret has been seen")
    secret = decrypt(secret_dict['secret'], ENCODING)
    delete_result = await db['secrets'].delete_one({"_id": secret_dict["_id"]})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content=secret)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Something went wrong")
