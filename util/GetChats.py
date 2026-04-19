import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient

from mongo.DB_Client import DB_Client
from util.Constants import DB
from util.TelegramMongo import TelegramMongo

load_dotenv()
tg_mongo = TelegramMongo(DB_Client().get_client())

api_id = tg_mongo.get_from_info(DB.API_ID)
api_hash = tg_mongo.get_from_info(DB.API_HASH)
cell_phone = tg_mongo.get_from_info(DB.CELL_PHONE)

#TODO change pass
client = TelegramClient('get_chats_session', api_id, api_hash).start(phone=cell_phone,password='****')

async def main():
    await client.start(cell_phone)

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        username = getattr(entity, DB.USERNAME, None)

        print(f"Chat Name: {dialog.name}")
        print(f"Chat ID: {dialog.id}")
        print(f"Username: @{username if username else '—'}")
        print(f"Type: {type(entity).__name__}")
        print("-" * 40)

# Run the client
with client:
    client.loop.run_until_complete(main())

if __name__ == "__main__":
    asyncio.run(main())