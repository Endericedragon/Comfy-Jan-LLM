import type { Window } from "./comfyApp";
const comfyApp = (window as unknown as Window).comfyAPI.app.app;

comfyApp.registerExtension({
    name: "endericedragon.comfy-jan-llm",
    settings: [
        {
            id: "comfy-jan-llm.api_key",
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
    ],
    async nodeCreated(node) {
        if (node.comfyClass !== "JanLLMApi") {
            return;
        }
        const ps = node.widgets?.find(w => w.name.includes("prompt_style"))!!;
        const sp = node.widgets?.find(w => w.name.includes("sys_prompt"))!!;
        sp.hidden = true;
        ps.callback = (val: string) => {
            if (val === "Customize") {
                sp.value = "";
                sp.hidden = false;
            } else {
                sp.hidden = true;
            }
        };
    },
    async setup() {
        console.log("Comfy-Jan-LLM is loaded!");
        await comfyApp.api.fetchApi("/jan-llm/set-api-key", {
            method: "POST",
            headers: { "Content-Type": "text/plain" },
            body: comfyApp.extensionManager.setting.get("api_key") || ""
        });
    }
})