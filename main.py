from typing import Annotated
from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from cryptocode import encrypt, decrypt
from config.settings import ENCODING_STRING
from config.database import db, create_ttl_index
from schemas import CreateSecretModel
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = FastAPI(
    title="Secret!"
)


create_ttl_index()


@app.post('/generate', response_description="Generated secret key", description="You can provide secret and "
                                                                                "secret-phrase for it, also you can "
                                                                                "provide timeToLive in sec("
                                                                                "default=3600).")
async def generate_secret_key(secret: CreateSecretModel = Body(...)):
    """
        param secret - is a pydantic model, there are four fields.
        return generated secret-key, which is needed for access to secret
    """
    secret = jsonable_encoder(secret)
    secret['secret'] = encrypt(secret['secret'], ENCODING_STRING)
    secret['phrase'] = generate_password_hash(secret['phrase'])
    secret['expire_at'] = datetime.utcnow() + timedelta(seconds=secret['timeToLive'])
    del secret['timeToLive']
    new_secret = await db["secrets"].insert_one(secret)
    secret_key = f"127.0.0.1:8000/secrets/{new_secret.inserted_id}"
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=secret_key)


@app.post('/secrets/{secret_key}', response_description="received secret, remember you can see it once, then it will "
                                                        "be deleted")
async def get_secret(secret_key: str, phrase: Annotated[str, Body()]):
    """
    :param secret_key: is used for accessing to secret
    :param phrase: is used for 'authentication', provides security of the secret
    :return: the secret, and then secret will be deleted
    """
    try:
        secret_dict = await db['secrets'].find_one({"_id": secret_key})
        if not check_password_hash(secret_dict['phrase'], phrase):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid secret phrase or secret key")
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")
    secret = decrypt(secret_dict['secret'], ENCODING_STRING)
    delete_result = await db['secrets'].delete_one({"_id": secret_dict["_id"]})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content=secret)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Something went wrong")
