from comfy_api.v0_0_2 import ComfyExtension, io, ui
import requests

from .jan_utils import DEFAULT_JAN_IP, JanAPI, JanConnect

jan_conn = JanConnect(DEFAULT_JAN_IP)


class JanLLMApi(io.ComfyNode):
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="JanLLMApi",
            display_name="Jan LLM API",
            inputs=[
                io.String.Input("jan_ip", "Jan Host IP", default=DEFAULT_JAN_IP),
                io.Combo.Input("model", jan_conn.get_models()),
                io.String.Input("prompt", default="Hello", multiline=True),
            ],
            outputs=[io.String.Output("opt_prompt", "Optimized Prompt")],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, **kwargs) -> io.NodeOutput:
        global jan_conn
        jan_url: str = kwargs["jan_ip"]
        jan_conn.jan_url = jan_url
        resp = requests.post(
            jan_conn.jan_url + JanAPI.CHAT.value,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer NewChannel123",
            },
            json={
                "model": "Jan-v3.5-4B-Q4_K_XL",
                "messages": [{"role": "user", "content": kwargs["prompt"]}],
            },
        )
        return io.NodeOutput(resp.text)


class JanLLMExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [JanLLMApi]


async def comfy_entrypoint() -> ComfyExtension:
    return JanLLMExtension()


__all__ = []
