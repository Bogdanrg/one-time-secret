import motor.motor_asyncio

MONGODB_URL = "mongodb://admin:admin@mongodb:27017/fastapi"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['fastapi']
