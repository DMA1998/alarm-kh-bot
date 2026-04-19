from typing import List

from pymongo import MongoClient

from dto.Channel import Channel
from util.Constants import DB


class TelegramMongo:

    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client.get_database(DB.DB_NAME)

    def get_chat_ids(self) -> List[str]:
        users_collection = self.db.get_collection(DB.USERS)
        user_documents = users_collection.find()
        return [user[DB.CHAT_ID] for user in user_documents]


    def get_from_info(self, value):
        info_collection = self.db.get_collection(DB.INFO)
        return info_collection.find_one().get(value)


    def add_subscriber(self, chat_id: str) -> None:
        users_collection = self.db.get_collection(DB.USERS)
        document = {DB.CHAT_ID: chat_id}
        users_collection.insert_one(document)


    def is_subscriber_exists(self, chat_id: int) -> bool:
        users_collection = self.db.get_collection(DB.USERS)
        search_criteria = {DB.CHAT_ID: chat_id}
        return users_collection.find_one(search_criteria) is not None

    def extract_channels(self) -> List[Channel]:
        channel_collection = self.db.get_collection(DB.CHANNEL)
        documents = channel_collection.find()
        return [Channel.from_dict(doc) for doc in documents]

    def extract_keywords(self) -> list[str]:
        keywords_collection = self.db.get_collection(DB.KEYWORDS)

        document = keywords_collection.find_one({"_id": DB.KEYWORDS})

        if not document or DB.WORDS not in document:
            raise ValueError("Keywords document not found in DB")

        return [word.lower() for word in document[DB.WORDS]]