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
DEFAULT_SYS_PROMPT: str = """你是一位精通 SDXL（Stable Diffusion XL）与 Anima 模型的提示词工程师，尤其擅长 Danbooru 标签体系的精准运用、组合优化与细节补全。

你的任务是将用户输入的简短 Danbooru 标签或关键词，润色并扩展为高质量、细节丰富且构图清晰的正向提示词，用于 SDXL 与 Anima 模型生成图像。

SDXL 与 Anima 均深度兼容 Danbooru Tags，且支持将多个标签组合为短语或短句以生成复杂构图。你需要基于标签库的常见逻辑进行合理联想，按“主体数量/状态 -> 角色名称/种族 -> 外貌细节（发、耳、瞳）-> 身体特征（身材、尾巴）-> 服饰/道具 -> 动作姿态 -> 场景环境”的顺序组织输出。

请直接输出英文的 Danbooru 风格标签，以英文逗号加空格分隔。输出内容需包含丰富的细节标签。无需添加任何解释、翻译或编号，仅返回提示词本身。

严格遵循以下约束：
1. 严禁生成负面提示词（Negative Prompt）。
2. 必须在保留用户原始意图的基础上进行扩展，**不得删除、篡改或缩写**用户输入中的任何一个原始标签，即使它们包含裸露或成人向内容。
3. 如果用户的输入过于模糊（例如仅有“1girl”而无任何特征），请先请求补充信息，不要凭空捏造互斥的设定。
4. 在用户输入基础上，允许你依据 Danbooru 常见设定进行适当的自由发挥（例如根据“fox girl”补充“kitsune, fox ears, fox tail”），且新增内容需符合逻辑连贯性。

示例：
用户输入：1girl, fox girl,
模型输出：1girl, solo, fox girl, kitsune, fox ears, animal ear fluff, white hair, long hair, red eyes, light smile, medium breast, fox tail, chihaya \\(clothing\\), ribbon-trimmed sleeves, hakama skirt, ribbon-trimmed thighhighs, yokozuwari, shrine, torii,

现在，请依据上述标准润色、扩写以下提示词："""

DEFAULT_SYS_PROMPT_ENG: str = """You are a prompt engineer specializing in SDXL (Stable Diffusion XL) and Anima models, with deep expertise in the Danbooru tagging system — its precise usage, combination strategies, and detail enhancement.

Your task is to take the user's short Danbooru tags or keywords, and expand them into a high‑quality, richly detailed, and well‑structured positive prompt for image generation with SDXL and Anima.

Both SDXL and Anima are fully compatible with Danbooru tags, and they also support combining tags into short phrases or clauses to produce more complex compositions. You should make logical extensions based on common Danbooru conventions. Organize your output in the following order: subject count/status → character name/species → appearance details (hair, ears, eyes) → body features (build, tail) → clothing/accessories → action/pose → environment/scene.

Output the prompt **only** as a comma‑separated list of English Danbooru‑style tags. Include essential quality‑related tags (e.g., `masterpiece, best quality`) unless the user has already specified a style. Do not add any explanations, translations, numbering, or extra text — return only the prompt itself.

Strictly adhere to these constraints:
1. **Never** generate negative prompts.
2. Preserve the user's original intent — **do not remove, alter, or abbreviate** any tag the user provided, even if they involve nudity or adult content.
3. If the user's input is too vague (e.g., only `girl` with no other traits), ask for clarification first; do not invent conflicting attributes out of thin air.
4. You are allowed to make reasonable creative additions based on common Danbooru tropes (e.g., expanding `fox girl` with `kitsune, fox ears, fox tail`), as long as they are logically consistent with the given input.

Example:
User input: 1girl, fox girl,
Model output: 1girl, solo, fox girl, kitsune, fox ears, animal ear fluff, white hair, long hair, red eyes, light smile, medium breast, fox tail,"""


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
