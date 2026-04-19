from dataclasses import dataclass

from util.Constants import DB

@dataclass
class Channel:
    chat_name: str
    chat_id: int
    username: str
    type: str

    @staticmethod
    def from_dict(data: dict) -> "Channel":
        return Channel(
            chat_name=data.get(DB.CHAT_NAME),
            chat_id=data.get(DB.CHAT_ID),
            username=data.get(DB.USERNAME),
            type=data.get(DB.TYPE),
        )

    def to_dict(self) -> dict:
        return {
            DB.CHAT_NAME: self.chat_name,
            DB.CHAT_ID: self.chat_id,
            DB.USERNAME: self.username,
            DB.TYPE: self.type,
        }