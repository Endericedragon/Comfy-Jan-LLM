const comfyApp = window.comfyAPI.app.app;
// import { app } from "../../scripts/app.js";

comfyApp.registerExtension({
    name: "endericedragon.comfy-jan-llm",
    settings: [
        {
            id: "api_key",
            name: "API Key for Jan LLM API",
            type: "text",
            defaultValue: "",
            onChange: async (nv, ov) => {
                await comfyApp.api.fetchApi("/jan-llm/set-api-key", {
                    method: "POST",
                    headers: { "Content-Type": "text/plain" },
                    body: nv
                });
            }
        }
    ]
})