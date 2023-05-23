import asyncio
from pyrogram.client import Client
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import random
from string import ascii_uppercase

print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(
    "mongodb+srv://techz:bots@cluster0.uzrha.mongodb.net/?retryWrites=true&w=majority"
)
print("[INFO]: SUCCESSFULLY CONNECTED TO MONGO DB")
db = mongo_client.techzapi

userdb = db.userdb


async def get_apikey(user_id):
    user = await userdb.find_one({"user_id": user_id})
    if user:
        return user.get("api_key")
    return False


async def get_user(user_id):
    return await userdb.find_one({"user_id": user_id})


async def create_newkey(user, reset=False):
    while True:
        key = "".join(random.choices(ascii_uppercase, k=6))
        if not await userdb.find_one({"api_key": key}):
            if reset:
                await userdb.update_one(
                    {"user_id": user}, {"$set": {"api_key": key}}, upsert=True
                )
            else:
                await userdb.update_one(
                    {"user_id": user},
                    {"$set": {"api_key": key, "used": 0, "credits": 20000}},
                    upsert=True,
                )
            return key


async def give_credits():
    await userdb.update_many({}, {"$set": {"credits": 10000}}, upsert=True)
    return True


async def broadcast():
    app = Client(
        "TechZBot",
        api_id=2344247,
        api_hash="853cae451f8091db916cd9ad395bbf12",
        bot_token="5817679103:AAFpywybrmzQTvToJXGptPYKxTu-nx7sSmI",
    )
    await app.start()
    async for user in userdb.find({}):
        try:
            user_id = user.get("user_id")
            await app.send_message(
                user_id,
                f"""**🎁 You Got 10k Credits More For Free This Month**

Need More Credits? Contact @TechZBots_Support""",
            )
            print(user_id, "Sent")
        except Exception as e:
            print(user_id, e)


# asyncio.run(broadcast())
# asyncio.run(give_credits())
