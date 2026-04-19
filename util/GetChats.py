import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient

from Bot import get_from_info
from mongo.DB_Client import DB_Client
from util.Constants import DB

load_dotenv()
mongo_client = DB_Client().get_client()
db = mongo_client.get_database(DB.DB_NAME)

api_id = get_from_info(DB.API_ID)
api_hash = get_from_info(DB.API_HASH)
cell_phone = get_from_info(DB.CELL_PHONE)

#TODO change pass
client = TelegramClient('get_chats_session', api_id, api_hash).start(phone=cell_phone,password='****')

async def main():
    await client.start(cell_phone)

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        username = getattr(entity, 'username', None)

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