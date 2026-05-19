import os

MODELS = {
    "DeepSeek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "api_key": os.environ.get("DEEPSEEK_API_KEY", "")
    },
    "通义千问": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo",
        "api_key": os.environ.get("QWEN_API_KEY", "")
    },
    "智谱GLM": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash",
        "api_key": os.environ.get("GLM_API_KEY", "")
    },
    "Kimi": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
        "api_key": os.environ.get("MOONSHOT_API_KEY", "")
    }
}

CATEGORIES = ["教育", "劳动", "校园", 其他"]
