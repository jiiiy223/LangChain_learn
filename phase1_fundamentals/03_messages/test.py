"""
测试脚本 - 验证对话历史管理
==============================
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

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


def test_conversation_memory():
    """测试 AI 是否记住对话"""
    print("\n测试：AI 对话记忆")
    print("="*50)

    conversation = [
        {"role": "system", "content": "你是助手"}
    ]

    # 告诉 AI 用户名字
    conversation.append({"role": "user", "content": "我叫李明"})
    r1 = model.invoke(conversation)
    conversation.append({"role": "assistant", "content": r1.content})
    print(f"用户: 我叫李明")
    print(f"AI: {r1.content[:50]}...")

    # 测试记忆
    conversation.append({"role": "user", "content": "我叫什么名字？"})
    r2 = model.invoke(conversation)
    print(f"\n用户: 我叫什么名字？")
    print(f"AI: {r2.content}")

    # 验证
    if "李明" in r2.content:
        print("\n✅ 测试通过：AI 记住了用户名字")
        return True
    else:
        print("\n❌ 测试失败：AI 忘记了用户名字")
        return False

def test_optimize_history():
    """测试历史优化函数"""
    print("\n\n测试：历史优化")
    print("="*50)

    def keep_recent_messages(messages, max_pairs=3):
        system_msgs = [m for m in messages if m.get("role") == "system"]
        conversation = [m for m in messages if m.get("role") != "system"]
        recent = conversation[-(max_pairs * 2):]
        return system_msgs + recent

    # 创建长历史
    long_conversation = [
        {"role": "system", "content": "你是助手"},
        {"role": "user", "content": "问题1"},
        {"role": "assistant", "content": "回答1"},
        {"role": "user", "content": "问题2"},
        {"role": "assistant", "content": "回答2"},
        {"role": "user", "content": "问题3"},
        {"role": "assistant", "content": "回答3"},
        {"role": "user", "content": "问题4"},
        {"role": "assistant", "content": "回答4"},
    ]

    print(f"原始消息数: {len(long_conversation)}")

    # 优化
    optimized = keep_recent_messages(long_conversation, max_pairs=2)
    print(f"优化后消息数: {len(optimized)}")

    # 验证
    expected = 1 + (2 * 2)  # system + 2轮对话
    if len(optimized) == expected:
        print(f"✅ 测试通过：保留了 system + 最近2轮")
        return True
    else:
        print(f"❌ 测试失败：期望 {expected} 条，实际 {len(optimized)} 条")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print(" 运行测试")
    print("="*50)

    results = []
    results.append(test_conversation_memory())
    results.append(test_optimize_history())

    print("\n" + "="*50)
    print(" 测试结果")
    print("="*50)
    print(f"通过: {sum(results)}/{len(results)}")

    if all(results):
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
