const comfyApp = window.comfyAPI.app.app;
// import { app } from "../../scripts/app.js";

comfyApp.registerExtension({
    name: "endericedragon.comfy-jan-llm",
    settings: [
        {
            id: "comfy-jan-llm.api_key",
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
    ],
    async setup() {
        console.log("Comfy-Jan-LLM is loaded!");
        await comfyApp.api.fetchApi("/jan-llm/set-api-key", {
            method: "POST",
            headers: { "Content-Type": "text/plain" },
            body: app.extensionManager.setting.get("api_key") || ""
        });
    }
})