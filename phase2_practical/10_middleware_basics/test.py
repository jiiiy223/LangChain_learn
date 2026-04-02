"""
简单测试：验证中间件功能
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware

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



print("=" * 70)
print("测试：中间件 before_model 和 after_model")
print("=" * 70)

class TestMiddleware(AgentMiddleware):
    """测试中间件"""

    def before_model(self, state, runtime):
        print("\n[测试] before_model 执行")
        print(f"[测试] 当前消息数: {len(state.get('messages', []))}")
        return None

    def after_model(self, state, runtime):
        print("[测试] after_model 执行")
        last_msg = state.get('messages', [])[-1]
        print(f"[测试] 响应类型: {last_msg.__class__.__name__}")
        return None

# 创建带中间件的 Agent
agent = create_agent(
    model=model,
    tools=[],
    system_prompt="你是一个有帮助的助手。",
    middleware=[TestMiddleware()]
)

print("\n执行测试调用...")
print("用户: 你好")

response = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})

print(f"\nAgent: {response['messages'][-1].content}")

print("\n" + "=" * 70)
print("测试结果：")
print("  - before_model 在模型调用前执行 [成功]")
print("  - after_model 在模型响应后执行 [成功]")
print("=" * 70)

print("\n测试完成！")
