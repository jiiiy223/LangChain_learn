"""
简单测试：验证内存功能
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

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
print("测试：InMemorySaver 内存功能")
print("=" * 70)

# 创建带内存的 Agent
agent = create_agent(
    model=model,
    tools=[],
    system_prompt="你是一个有帮助的助手。",
            checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id": "test_session"}}

print("\n第一轮对话：")
print("用户: 我叫张三")
response1 = agent.invoke(
    {"messages": [{"role": "user", "content": "我叫张三"}]},
    config=config
)
print(f"Agent: {response1['messages'][-1].content}")

print("\n第二轮对话：")
print("用户: 我叫什么？")
response2 = agent.invoke(
    {"messages": [{"role": "user", "content": "我叫什么？"}]},
    config=config
)
print(f"Agent: {response2['messages'][-1].content}")

print("\n" + "=" * 70)
print("内存状态：")
print(f"  总消息数: {len(response2['messages'])}")
print(f"  thread_id: {config['configurable']['thread_id']}")
print("=" * 70)

if "张三" in response2['messages'][-1].content:
    print("\n测试成功！Agent 记住了名字。")
else:
    print("\n警告：Agent 可能没有正确记住")

print("\n测试完成！")
