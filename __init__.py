from comfy_api.v0_0_2 import ComfyExtension, io
from aiohttp import web
from server import PromptServer

from .jan_utils import DEFAULT_JAN_URL, DEFAULT_SYS_PROMPT, JanConnect

jan_conn = JanConnect(DEFAULT_JAN_URL, "")


class JanLLMApi(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="JanLLMApi",
            display_name="Jan LLM API",
            inputs=[
                io.String.Input("jan_addr", "Jan Address", default=DEFAULT_JAN_URL),
                io.Combo.Input("model", jan_conn.get_models()),
                io.String.Input(
                    "sys_prompt", default=DEFAULT_SYS_PROMPT, multiline=True
                ),
                io.String.Input("prompt", default="1girl, solo,", multiline=True),
            ],
            outputs=[io.String.Output("opt_prompt", "Optimized Prompt")],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        global jan_conn
        jan_conn.jan_url = kwargs["jan_addr"]
        res = jan_conn.chat(kwargs["model"], kwargs["sys_prompt"], kwargs["prompt"])
        return io.NodeOutput(res)


class JanLLMExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [JanLLMApi]


async def comfy_entrypoint() -> ComfyExtension:
    return JanLLMExtension()


@PromptServer.instance.routes.post("/jan-llm/set-api-key")
async def set_api_key(request: web.Request) -> web.Response:
    global jan_conn
    api_key = await request.text()
    jan_conn.api_key = api_key
    return web.Response(status=200)


WEB_DIRECTORY = "./web"
__all__ = ["WEB_DIRECTORY"]
