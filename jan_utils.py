import sys
from enum import Enum
from pathlib import Path
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


DEFAULT_JAN_URL: str = "http://127.0.0.1:1337/v1"
USE_NO_LLM: str = "Off"


class JanAPI(Enum):
    CHAT = "/chat/completions"
    MODELS = "/models"


class JanConnect:
    def __init__(self, jan_url: str, api_key: str):
        self.jan_url = jan_url
        self.api_key = api_key

    def get_models(self) -> List[str]:
        res = [USE_NO_LLM]
        try:
            resp = requests.get(
                self.jan_url + JanAPI.MODELS.value,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.api_key),
                },
                timeout=1,  # 快操作
            )
            assert resp.status_code == 200
            info: RespModels = resp.json()
            res.extend(list(map(lambda x: x["id"], info["data"])))
        except Exception as e:
            print(type(e), e, file=sys.stderr)
        finally:
            return res

    def chat(self, model: str, sys_prompt: str, prompt: str) -> str:
        if model == USE_NO_LLM:
            return prompt
        full_prompt = sys_prompt + "\n\n" + prompt
        resp = requests.post(
            self.jan_url + JanAPI.CHAT.value,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.api_key),
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": full_prompt}],
            },
        )
        assert resp.status_code == 200
        return resp.json()["choices"][0]["message"]["content"]
