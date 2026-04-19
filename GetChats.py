import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.functions.messages import GetDialogFiltersRequest

from Bot import get_from_info
from mongo.DB_Client import DB_Client
from util.Constants import TgClient, DB

load_dotenv()
mongo_client = DB_Client().get_client()
db = mongo_client.get_database(DB.DB_NAME)

api_id = get_from_info(DB.API_ID)
api_hash = get_from_info(DB.API_HASH)
cell_phone = get_from_info(DB.CELL_PHONE)

# async def main():
#     async with TelegramClient("real_user_session", api_id, api_hash) as client:
#         await client.start(phone=cell_phone)
#
#         me = await client.get_me()
#         print(f"Logged in as: id={me.id}, bot={getattr(me, 'bot', False)}, username={getattr(me, 'username', None)}")
#         print("=== All chats ===")
#
#         async for dialog in client.iter_dialogs():
#             chat = dialog.entity
#             print(f"chat_id: {dialog.id}")
#             print(f"type: {type(chat).__name__}")
#             print(f"title: {dialog.name}")
#             print(f"username: @{getattr(chat, 'username', None) or '—'}")
#             print("-" * 40)

# Initialize the client
#TODO change pass
client = TelegramClient('get_chats_session', api_id, api_hash).start(phone=cell_phone,password='****')

async def main():
    # Connect to Telegram
    await client.start(cell_phone)
    print("Logged in successfully!")

    # Get the list of dialogs (chats/groups)
    async for dialog in client.iter_dialogs():
        #print(f"Chat Name: {dialog.name}, Chat ID: {dialog.id}, {dialog}")

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