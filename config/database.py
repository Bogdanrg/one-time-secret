import motor.motor_asyncio

MONGODB_URL = "mongodb://admin:admin@localhost:27018/FastAPI?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.FastAPI
