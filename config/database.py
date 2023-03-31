import motor.motor_asyncio

MONGODB_URL = "mongodb://admin:admin@mongodb:27017/fastapi"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['fastapi']


# creating TTL index
def create_ttl_index():
    db["secrets"].create_index([("expire_at", 1)], expireAfterSeconds=0)
