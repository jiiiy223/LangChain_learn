"""
简单测试：验证 Agent 可以正常工作
"""

import os
import sys

# 添加工具目录到路径
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(parent_dir, '04_custom_tools', 'tools'))

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from weather import get_weather
from calculator import calculator

# 加载环境变量
load_dotenv()
CHAT_MODEL = os.getenv("CHAT_MODEL", "openai:qwen-plus")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

PROVIDER_API_KEY_ENV = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "google_genai": "GOOGLE_API_KEY",
    "google_vertexai": "GOOGLE_API_KEY",
}

provider = CHAT_MODEL.split(":", 1)[0]
MODEL_INIT_KWARGS = {}

if provider == "openai" and "qwen" in CHAT_MODEL.lower():
    if not DASHSCOPE_API_KEY or DASHSCOPE_API_KEY.startswith("your_"):
        raise ValueError(
            "\n请先在 .env 文件中设置有效的 DASHSCOPE_API_KEY\n"
            "当前默认使用阿里云千问模型（DashScope OpenAI 兼容模式）"
        )

    MODEL_INIT_KWARGS = {
        "api_key": DASHSCOPE_API_KEY,
        "base_url": OPENAI_BASE_URL,
    }
else:
    api_key_env = PROVIDER_API_KEY_ENV.get(provider)
    api_key_value = os.getenv(api_key_env) if api_key_env else None

    if api_key_env and (not api_key_value or api_key_value.startswith("your_")):
        raise ValueError(
            f"\n请先在 .env 文件中设置有效的 {api_key_env}\n"
            f"当前 CHAT_MODEL={CHAT_MODEL}"
        )

def create_chat_model(model_name=None, **kwargs):
    return init_chat_model(model_name or CHAT_MODEL, **MODEL_INIT_KWARGS, **kwargs)

model = create_chat_model()



print("创建 Agent...")
agent = create_agent(
    model=model,
    tools=[get_weather, calculator],
    system_prompt="你是一个helpful assistant。"
)

print("\n测试1：天气查询")
response1 = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气如何？"}]
})
print(f"回答：{response1['messages'][-1].content}\n")

print("测试2：计算")
response2 = agent.invoke({
    "messages": [{"role": "user", "content": "10 加 20 等于多少？"}]
})
print(f"回答：{response2['messages'][-1].content}\n")

print("测试成功！Agent 可以正常调用工具。")
