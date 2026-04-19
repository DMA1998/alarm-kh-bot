import os
from typing import List
from dotenv import load_dotenv
from telethon import TelegramClient, events

from dto.Channel import Channel
from util.Constants import DB,TgClient
from mongo.DB_Client import DB_Client

#TODO change loadenv only for local run

load_dotenv()
mongo_client = DB_Client().get_client()
db = mongo_client.get_database(DB.DB_NAME)

#TODO get the list of all chats to get chat_id and name and make posible to search by chat id
#TODO figure out problem with 2Auth (verification by the internal code)

def get_chat_ids() -> List[str]:
    users_collection = db.get_collection(DB.USERS)
    user_documents = users_collection.find()
    return [user[DB.CHAT_ID] for user in user_documents]


def get_from_info(value):
    info_collection = db.get_collection(DB.INFO)
    return info_collection.find_one().get(value)


def start_client(client: TelegramClient):
    client.start()
    print('Client successfully Started')
    client.run_until_disconnected()


def add_subscriber(chat_id: str) -> None:
    users_collection = db.get_collection(DB.USERS)
    document = {DB.CHAT_ID: chat_id}
    users_collection.insert_one(document)


def is_subscriber_exists(chat_id) -> bool:
    users_collection = db.get_collection(DB.USERS)
    search_criteria = {DB.CHAT_ID: chat_id}
    return users_collection.find_one(search_criteria) is not None

def extract_channels() -> List[Channel]:
    channel_collection = db.get_collection(DB.CHANNEL)
    documents = channel_collection.find()
    return [Channel.from_dict(doc) for doc in documents]

def extract_keywords() -> list[str]:
    keywords_collection = db.get_collection(DB.KEYWORDS)

    document = keywords_collection.find_one({"_id": DB.KEYWORDS})

    if not document or DB.WORDS not in document:
        raise ValueError("Keywords document not found in DB")

    return [word.lower() for word in document[DB.WORDS]]



#TODO move to DB and change to chat_id as it more stable and works for private channels as well
channels: List[Channel] = extract_channels()
chat_ids = [channel.chat_id for channel in channels]
api_id = get_from_info(DB.API_ID)
api_hash = get_from_info(DB.API_HASH)
cell_phone = get_from_info(DB.CELL_PHONE)
bot_token = get_from_info(DB.BOT_TOKEN)

if __name__ == "__main__":
    tg_2f_pass = os.environ.get('2F_PASS')
    user_client = TelegramClient(TgClient.USER_CLIENT, api_id, api_hash).start(phone=cell_phone, password=tg_2f_pass)
    bot_client = TelegramClient(TgClient.BOT_CLIENT, api_id, api_hash).start(bot_token=bot_token)

    commands_list = ["/start", "/help"]


    @bot_client.on(events.NewMessage(pattern='/start'))
    async def start(message):
        chat_id = message.chat_id
        if not is_subscriber_exists(chat_id):
            add_subscriber(chat_id)
            await bot_client.send_message(chat_id, 'Бот активован ✅')
        else:
            await bot_client.send_message(chat_id, 'Бот вже активован ❗')


    @bot_client.on(events.NewMessage(pattern='/help'))
    async def helps(message):
        chat_id = message.chat_id
        reply_message = "/start - активувати бота"
        await bot_client.send_message(chat_id, reply_message)


    @bot_client.on(events.NewMessage())
    async def command(message):
        text = message.message.raw_text

        if text not in commands_list:
            chat_id = message.chat_id
            reply_message = 'Введіть /help, щоб переглянути всі доступні команди'
            await bot_client.send_message(chat_id, reply_message)


#TODO move to database
    keywords = extract_keywords()

    @user_client.on(events.NewMessage(chats=chat_ids))
    async def message_handler(event):
        message = event.message.message

        message_in_lowercase = str(message).lower()

        found_keywords = [keyword for keyword in keywords if keyword in message_in_lowercase]

        if found_keywords:
            #TODO retrieve name by chat id from DB
            event_chat_id = event.message.chat_id
            sender = next((c.chat_name for c in channels if c.chat_id == event_chat_id), "Невідомо")
            for chat_id in get_chat_ids():
                await bot_client.send_message(chat_id, f'{message}\n❗❗❗😱\nДжерело: {sender}')

    print('Bot instance is running')

    start_client(user_client)
