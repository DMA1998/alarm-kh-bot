import os

from pymongo import MongoClient


class Mongo:

    def __init__(self):
        self.__hostname: str = os.environ.get('MONGO_HOSTNAME')
        self.__port: int = int(os.environ.get('MONGO_PORT'))
        self.__username: str = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
        self.__password: str = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')

    def get_client(self) -> MongoClient:
        connection_string = f'mongodb://{self.__username}:{self.__password}@{self.__hostname}:{self.__port}'
        return MongoClient(connection_string)
