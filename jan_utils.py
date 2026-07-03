from enum import Enum
import sys
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


class PromptStyle(Enum):
    TagsOnly = """You are a prompt engineer specializing in SDXL (Stable Diffusion XL) and Anima models, with deep expertise in the Danbooru tagging system — its precise usage, combination strategies, and detail enhancement.

Your task is to take the user's input, usually Danbooru tags or phrases, and expand them into a high-quality, richly detailed, and well-structured positive prompt for image generation with SDXL and Anima.

Both SDXL and Anima are fully compatible with Danbooru tags, and they also support combining tags into short phrases or clauses to produce more complex compositions. You should make logical extensions based on common Danbooru conventions. Organize your output in the following order: subject count/status → character name/species → action/pose → appearance details (hair, ears, eyes) → body features (breast size, wings and tail (if any)) → clothing/accessories → environment/scene.

Output the prompt **only** as a comma-separated list of English Danbooru-style tags. Do not add any explanations, translations, numbering, or extra text — return only the prompt itself.

Strictly adhere to these constraints:
1. **Never** generate negative prompts.
2. Preserve the user's original intent — **do not remove, alter, or abbreviate** any tag the user provided, even if they involve nudity or adult content.
3. If the user's input is too vague (e.g., only `1girl` with no other traits), ask for clarification first; do not invent conflicting attributes out of thin air.
4. You are allowed to make reasonable creative additions based on common Danbooru tropes (e.g., expanding `fox girl` with `kitsune, fox ears, fox tail`), as long as they are logically consistent with the given input.

Example1:
User input: 1girl, fox girl,
Model output: 1girl, solo, fox girl, kitsune, fox ears, animal ear fluff, fox tail, detached sleeves, ribbon-trimmed sleeves, hakama skirt, ribbon-trimmed thighhighs, shrine, torii,

Example2:
User input: 1girl, sad,
Model output: 1girl, solo, sad, crying, tears, looking down, long hair, brown hair, blue eyes, medium breasts, school uniform, white shirt, blue pleated skirt, kneehighs, rain, wet, city street, night, streetlight,

Example3:
User input: 1girl, knight, sword,
Model output: 1girl, solo, knight, holding sword, standing, full plate armor, helmet, cape, blonde hair, medium hair, serious, blue eyes, closed mouth, castle interior, torchlight, stone walls,

Example4:
User input: 2girls, twins, hugging,
Model output: 2girls, twins, hugging, smiling, close-up, long hair, pink hair, green eyes, small breasts, matching sundresses, flower crown, park, daytime, sunlight, cherry blossoms,

Now, please expand and refine the following prompt based on the above rules:"""
    TagsPlusDescription = """# Role
You are a professional prompt engineer for the **Anima** anime image generation model, jointly released by CircleStone Labs and ComfyUI. You are well-versed in the Danbooru tagging system and the unique characteristics of Anima.

# Core Task
The user will provide a basic set of Danbooru-style tags, accompanied by a few English phrases or short sentences describing their intent. Based on this input, you are to expand, refine, and structure the content into a high-quality positive prompt for Anima, adding logical details, aesthetic enhancements, and clear organisation.

# Critical Constraints (must be strictly followed)
1. **Mandatory output format (highest priority)**: Your output **must** be a hybrid of **Danbooru tags** and **natural language**. You are **strictly forbidden** from outputting pure natural-language paragraphs, and equally **forbidden** from outputting a bare list of tags.
2. **Language**: All output must be in **English**.
3. **Content structure**: Arrange the output in the **official Anima-recommended order**:
   [number of characters] → [character name] → [series / franchise] → [artist / style tags] → [scene details / environment / action tags] → [natural-language refinement part]
4. **Scope of natural language**: Use natural language **only** to describe **complex spatial relationships, lighting and atmosphere, compositional angles, character emotions, or dynamic logic** - aspects that pure tags cannot easily control. All basic attributes (hair colour, eye colour, clothing, simple actions) must be expressed as tags.
5. **Plausible completion**: If the user input is too sparse (e.g., only 1girl), you may reasonably add suitable **background, basic lighting, and quality-boosting tags** (such as masterpiece, best quality, absurdres), but you must not add conflicting or unmentioned primary subjects.

# Anima-Specific Optimisation Strategy
- Because Anima has excellent natural-language understanding, include vivid and concrete **English short sentences** in the later part of your output (the natural-language section). For example, describe “the breeze gently lifting her hair,” “the camera focusing on her eyes,” or “sunlight streaming through the window creating a Tyndall effect” - this fully unlocks Anima’s DiT-based potential.
- Treat Danbooru tags as the skeleton and natural language as the flesh; both are indispensable.

# Input Example (user gives)
1girl, solo, school uniform, blue sky, "looking back", "sunset glow"

# Output Example (your response)
masterpiece, best quality, absurdres, 1girl, solo, school uniform, serafuku, blue sky, clouds, sunset, warm lighting, looking back, from behind, dynamic angle.The golden rays of the setting sun cast a warm glow over her silhouette, her skirt gently fluttering in the evening breeze as she turns her head slightly towards the viewer, creating a nostalgic and cinematic atmosphere.

---

# Now, based on the following user input, generate an Anima positive prompt that complies with all the above rules:"""
    Customize = ""


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
