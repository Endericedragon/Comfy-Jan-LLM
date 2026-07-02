import { type Window } from "./types/comfyApi"

const cuWin = window as unknown as Window;
const comfyApp = cuWin.comfyAPI.app.app;

comfyApp.registerExtension({
    name: "endericedragon.comfy-jan-llm",
    settings: [
        {
            id: "api_key",
            name: "API Key for Jan LLM API",
            type: "text",
            defaultValue: "",
            onChange: async (nv: string, _ov: string) => {
                await comfyApp.api.fetchApi("/jan-llm/set-api-key", {
                    method: "POST",
                    headers: { "Content-Type": "text/plain" },
                    body: nv
                });
            }
        }
    ]
})