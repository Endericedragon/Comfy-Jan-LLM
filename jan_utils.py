from enum import Enum
from typing import List, TypedDict
import requests


class RespModelData(TypedDict):
    created: int
    id: str
    object: str
    owned_by: str


class RespModels(TypedDict):
    data: List[RespModelData]
    object: str


DEFAULT_JAN_IP: str = "http://127.0.0.1:1337/v1"


class JanAPI(Enum):
    CHAT = "/chat/completions"
    MODELS = "/models"


class JanConnect:
    def __init__(self, jan_url: str = DEFAULT_JAN_IP):
        self.jan_url = jan_url

    def get_models(self) -> List[str]:
        resp = requests.get(
            self.jan_url + JanAPI.MODELS.value,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer NewChannel123",
            },
        )
        if resp.status_code == 200:
            info: RespModels = resp.json()
            return list(map(lambda x: x["id"], info["data"]))
        else:
            print(resp.status_code, resp.text)
            return []
    
    def chat(self, model: str, prompt: str) -> str:
        resp = requests.post(
            self.jan_url + JanAPI.CHAT.value,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer NewChannel123",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            print(resp.status_code, resp.text)
            return ""
