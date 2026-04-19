import os
from typing import List
from dotenv import load_dotenv
from telethon import TelegramClient, events

from dto.Channel import Channel
from util.Constants import DB,TgClient
from mongo.DB_Client import DB_Client
from util.TelegramMongo import TelegramMongo

#TODO change loadenv only for local run

load_dotenv()
tg_mongo = TelegramMongo(DB_Client().get_client())

def start_client(client: TelegramClient):
    client.start()
    print('Client successfully Started')
    client.run_until_disconnected()

channels: List[Channel] = tg_mongo.extract_channels()
chat_ids = [channel.chat_id for channel in channels]
api_id = tg_mongo.get_from_info(DB.API_ID)
api_hash = tg_mongo.get_from_info(DB.API_HASH)
cell_phone = tg_mongo.get_from_info(DB.CELL_PHONE)
bot_token = tg_mongo.get_from_info(DB.BOT_TOKEN)

if __name__ == "__main__":
    tg_2f_pass = os.environ.get('2F_PASS')
    user_client = TelegramClient(TgClient.USER_CLIENT, api_id, api_hash).start(phone=cell_phone, password=tg_2f_pass)
    bot_client = TelegramClient(TgClient.BOT_CLIENT, api_id, api_hash).start(bot_token=bot_token)

    commands_list = ["/start", "/help"]

    @bot_client.on(events.NewMessage(pattern='/start'))
    async def start(message):
        chat_id = message.chat_id
        if not tg_mongo.is_subscriber_exists(chat_id):
            tg_mongo.add_subscriber(chat_id)
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

    keywords = tg_mongo.extract_keywords()

    @user_client.on(events.NewMessage(chats=chat_ids))
    async def message_handler(event):
        message = event.message.message

        message_in_lowercase = str(message).lower()

        found_keywords = [keyword for keyword in keywords if keyword in message_in_lowercase]

        if found_keywords:
            event_chat_id = event.message.chat_id
            sender = next((c.chat_name for c in channels if c.chat_id == event_chat_id), "Невідомо")
            for chat_id in tg_mongo.get_chat_ids():
                await bot_client.send_message(chat_id, f'{message}\n❗❗❗😱\nДжерело: {sender}')

    print('Bot instance is running')

    start_client(user_client)
