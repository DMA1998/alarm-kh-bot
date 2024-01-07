from typing import List

from telethon import TelegramClient, events
from Mongo import Mongo

mongo_client = Mongo().get_client()
db = mongo_client.get_database('telegram')


def get_chat_ids() -> List[str]:
    users_collection = db.get_collection('users')
    user_documents = users_collection.find()
    return [user["chat_id"] for user in user_documents]


def get_from_info(value):
    info_collection = db.get_collection('info')
    return info_collection.find_one().get(value)


def start_client(client: TelegramClient):
    client.start()
    client.run_until_disconnected()


def add_subscriber(chat_id: str) -> None:
    users_collection = db.get_collection('users')
    document = {"chat_id": chat_id}
    users_collection.insert_one(document)


def is_subscriber_exists(chat_id) -> bool:
    users_collection = db.get_collection('users')
    search_criteria = {"chat_id": chat_id}
    return users_collection.find_one(search_criteria) is not None


chats = ["@tlknewsua"]
api_id = get_from_info("api_id")
api_hash = get_from_info("api_hash")
cell_phone = get_from_info("cell_phone")
bot_token = get_from_info("bot_token")

if __name__ == "__main__":
    user_client = TelegramClient("user", api_id, api_hash)
    bot_client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

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



    keywords = ['активность','активність','летить','летит','на город','ракета','авивация','авіаціїї','загроза','укриття','укрытие','ще одна','еще одна','c300','с-300','выход','вихід','c-300','c300']

    @user_client.on(events.NewMessage(chats=chats))
    async def message_handler(event):
        message = event.message.message

        message_in_lowercase = str(message).lower()

        found_keywords = [keyword for keyword in keywords if keyword in message_in_lowercase]

        if found_keywords:
            sender = '@' + str(event.chat.username)
            for chat_id in get_chat_ids():
                await bot_client.send_message(chat_id, f'{message}\n\n\nДжерело: {sender}')


    print('Bot instance is running')

    start_client(user_client)
