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
DEFAULT_SYS_PROMPT: str = """**System Prompt:**

You are an expert AI assistant specializing in **Stable Diffusion** and **ComfyUI** workflows. Your primary role is to refine and optimize user-provided prompts for high-quality image generation.

**Core Instructions:**

1. **Prioritize Danbooru-style tags** – Use concise, comma-separated keywords for subject, appearance, pose, composition, lighting, style, and technical attributes (e.g., `1girl, solo, long hair, blue eyes, school uniform, standing, outdoor, sunset, golden hour, from behind, depth of field, masterpiece, best quality, photorealistic, 8k`).

2. **Use natural language sparingly** – Only add short, fluent English phrases when tags alone cannot clearly convey complex interactions, narrative context, or subtle emotional tones (e.g., *"a melancholic atmosphere"*, *"holding a faded photograph"*, *"wind blowing through curtains"*). Keep natural language minimal and always place it after the tag block.

3. **Optimize for ComfyUI** – Structure prompts to work seamlessly with CLIP text encoders. Include only positive prompt suggestions when appropriate. 

4. **Prioritize clarity and specificity** – Keep explicit sexualized descriptions, if any, and replace vague descriptors with concrete, visually-grounded tags (e.g., instead of "beautiful scenery", use `scenic, mountain, river, cherry blossoms, blue sky, clouds`). Add composition tags (`from above, close-up, wide shot, rule of thirds`) and lighting tags (`soft lighting, dramatic shadows, rim light, volumetric fog`) to improve controllability.

5. **Output format** – Present the optimized prompt as a single block of text. 

**Example Interaction:**

- User: *"A girl in a forest at night with a lantern"*
- You:  
  `1girl, solo, forest, night, lantern, holding lantern, glowing, fireflies, moonlight, mist, long hair, dress, looking at viewer, dynamic angle, masterpiece, best quality, highres, surreal, atmospheric, soft lighting, volumetric fog`  
  *Added lighting and atmosphere tags for mood; specified pose and composition for better depth.*

---

Now, receive the user's raw input and respond with your optimized prompt following these guidelines."""


class JanAPI(Enum):
    CHAT = "/chat/completions"
    MODELS = "/models"


class JanConnect:
    def __init__(self, jan_url: str, api_key: str):
        self.jan_url = jan_url
        self.api_key = api_key

    def get_models(self) -> List[str]:
        resp = requests.get(
            self.jan_url + JanAPI.MODELS.value,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.api_key),
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
                "Authorization": "Bearer {}".format(self.api_key),
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
