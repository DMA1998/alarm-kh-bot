from dataclasses import dataclass


@dataclass
class Channel:
    chat_name: str
    chat_id: int
    username: str
    type: str

    @staticmethod
    def from_dict(data: dict) -> "Channel":
        return Channel(
            chat_name=data.get("chat_name"),
            chat_id=data.get("chat_id"),
            username=data.get("username"),
            type=data.get("type"),
        )

    def to_dict(self) -> dict:
        return {
            "chat_name": self.chat_name,
            "chat_id": self.chat_id,
            "username": self.username,
            "type": self.type,
        }