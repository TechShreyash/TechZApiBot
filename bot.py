from pyrogram.types import Message
from pyrogram import Client, filters, idle
from pyrogram.client import Client
import asyncio
from uvloop import install
from utils.database import create_newkey, get_apikey, get_user
from contextlib import closing, suppress

app = Client(
    "TechZBot",
    api_id=2344247,
    api_hash="853cae451f8091db916cd9ad395bbf12",
    bot_token="5817679103:AAEhbhsOHZP0giq0gnVFM1g6KyJz0EhbScU",
)


async def isUserJoined(user):
    try:
        chat = await app.get_chat_member("TechZBots", user)
        chat = await app.get_chat_member("TechZBots_Support", user)
        return True
    except:
        return False


@app.on_message(filters.command(["start", "help"]) & filters.incoming & filters.private)
async def start(client, message: Message):
    if not await isUserJoined(message.from_user.id):
        return await message.reply_text(
            """**You must join our Updates Channel and Support Group**

Updates Channel : @TechZBots
Support Group : @TechZBots_Support""",
        )
    await message.reply_text(
        """**⛩ Hello, I am a simple bot to get your Api Key for using TechZApi.**
        
To get your API key, use the /api_key command.
To reset you Api Key, use the /reset command.
To check your credits, use the /credits command.
        
If you have any questions, contact @TechZBots_Support""",
    )


@app.on_message(filters.command(["api_key"]) & filters.incoming & filters.private)
async def api_key(client, message: Message):
    user = message.from_user.id
    if not await isUserJoined(user):
        return await message.reply_text(
            """**You must join our Updates Channel and Support Group**

Updates Channel : @TechZBots
Support Group : @TechZBots_Support""",
        )

    key = await get_apikey(user)
    if key:
        return await message.reply_text(
            f"""**♻️ Your Api Key is** `{key}`
            
Use /reset to reset your api key

Documentation: https://api1.techzbots.live/docs
Support: @TechZBots_Support""",
        )

    key = await create_newkey(user)
    await message.reply_text(
        f"""**✅ Generated New Api Key**
        
**Your Api Key is** `{key}`
        
Use /reset to reset your api key

Documentation: https://api1.techzbots.live/docs
Support: @TechZBots_Support"""
    )
    await asyncio.sleep(1)
    await message.reply_text(
        """🎁 You got 1000 credits for free
    
Note: You will get 1000 credits every day for free, To get more credits, contact @TechZBots_Support"""
    )


@app.on_message(filters.command(["reset"]) & filters.incoming & filters.private)
async def reset(client, message: Message):
    if not await isUserJoined(message.from_user.id):
        return await message.reply_text(
            """**You must join our Updates Channel and Support Group**

Updates Channel : @TechZBots
Support Group : @TechZBots_Support""",
        )

    user = message.from_user.id
    key = await get_apikey(user)
    if not key:
        return await message.reply_text(
            "You don't have an api key, use /api_key to get one",
        )

    key = await create_newkey(user, reset=True)
    await message.reply_text(
        f"""**✅ Generated New Api Key**
        
**Your Api Key is** `{key}`
        
Use /reset to reset your api key

Documentation: https://api1.techzbots.live/docs
Support: @TechZBots_Support"""
    )


@app.on_message(filters.command(["credits"]) & filters.incoming & filters.private)
async def credits(client, message: Message):
    if not await isUserJoined(message.from_user.id):
        return await message.reply_text(
            """**You must join our Updates Channel and Support Group**

Updates Channel : @TechZBots
Support Group : @TechZBots_Support""",
        )

    user = message.from_user.id
    data = await get_user(user)
    if not data:
        return await message.reply_text(
            """**You don't have an api key, use /api_key to get one**""",
        )

    await message.reply_text(
        f"""**🎁 You have {data.get('credits')} credits left this month**
        
**Used:** {data.get('used')} credits

To get more credits, contact @TechZBots_Support

**Price:** 1 Rs = 1000 credits
"""
    )


async def main():
    await app.start()
    print("[INFO]: BOT STARTED")
    await idle()
    print("[INFO]: BOT STOPPED")
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel()


loop = asyncio.get_event_loop()

if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(main())
            loop.run_until_complete(asyncio.sleep(3.0))
