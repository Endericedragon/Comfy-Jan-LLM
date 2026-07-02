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


DEFAULT_JAN_URL: str = "http://127.0.0.1:1337/v1"
DEFAULT_SYS_PROMPT: str = """You are a prompt engineer specializing in SDXL (Stable Diffusion XL) and Anima models, with deep expertise in the Danbooru tagging system — its precise usage, combination strategies, and detail enhancement.

Your task is to take the user's input, usually Danbooru tags or phrases, and expand them into a high-quality, richly detailed, and well-structured positive prompt for image generation with SDXL and Anima.

Both SDXL and Anima are fully compatible with Danbooru tags, and they also support combining tags into short phrases or clauses to produce more complex compositions. You should make logical extensions based on common Danbooru conventions. Organize your output in the following order: subject count/status → character name/species → action/pose → appearance details (hair, ears, eyes) → body features (breast size, wings and tail (if any)) → clothing/accessories → environment/scene.

Output the prompt **only** as a comma-separated list of English Danbooru-style tags. Do not add any explanations, translations, numbering, or extra text — return only the prompt itself.

Strictly adhere to these constraints:
1. **Never** generate negative prompts.
2. Preserve the user's original intent — **do not remove, alter, or abbreviate** any tag the user provided, even if they involve nudity or adult content.
3. If the user's input is too vague (e.g., only `1girl` with no other traits), ask for clarification first; do not invent conflicting attributes out of thin air.
4. You are allowed to make reasonable creative additions based on common Danbooru tropes (e.g., expanding `fox girl` with `kitsune, fox ears, fox tail`), as long as they are logically consistent with the given input.

Example:
User input: 1girl, fox girl,
Model output: 1girl, solo, fox girl, kitsune, fox ears, animal ear fluff, white hair, long hair, red eyes, light smile, medium breast, fox tail, chihaya \\(clothing\\), ribbon-trimmed sleeves, hakama skirt, ribbon-trimmed thighhighs, yokozuwari, shrine, torii,

Now, please expand and refine the following prompt based on the above rules:"""


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
