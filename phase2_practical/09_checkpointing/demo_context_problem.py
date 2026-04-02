"""
演示：对话历史过长的问题
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver

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



def demo_long_conversation():
    """
    演示：对话历史过长的问题
    """
    print("\n" + "="*70)
    print(" 演示：对话历史过长的性能问题")
    print("="*70)

    db_path = "long_conversation.sqlite"

    with SqliteSaver.from_conn_string(f"sqlite:///{db_path}") as checkpointer:
        agent = create_agent(
            model=model,
            tools=[],
            system_prompt="你是一个有帮助的助手。",
            checkpointer=checkpointer
        )

        config = {"configurable": {"thread_id": "test_user"}}

        # 模拟 50 轮对话
        print("\n[模拟 50 轮对话...]")
        for i in range(1, 51):
            agent.invoke(
                {"messages": [{"role": "user", "content": f"这是第 {i} 条消息"}]},
                config=config
            )
            if i % 10 == 0:
                print(f"  已完成 {i} 轮...")

        print("\n[尝试获取状态，查看加载的消息数量...]")

        # 获取当前状态
        state = checkpointer.get(config)
        if state and state.values:
            messages = state.values.get("messages", [])
            print(f"\n⚠️ 当前加载的消息数量：{len(messages)}")
            print(f"⚠️ 这意味着每次 invoke 都会加载这么多消息！")

            # 计算大致的 Token 数（简化估算）
            total_chars = sum(len(str(msg)) for msg in messages)
            estimated_tokens = total_chars // 4  # 粗略估算
            print(f"⚠️ 估算 Token 数：~{estimated_tokens}")

            print("\n问题：")
            print("  1. 随着对话增长，每次加载的数据越来越多")
            print("  2. 超过模型上下文窗口限制会报错")
            print("  3. 性能下降，响应变慢")
            print("  4. Token 费用增加")

    # 清理
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\n[已清理测试数据库]")

def show_solutions():
    """
    展示解决方案
    """
    print("\n" + "="*70)
    print(" 解决方案")
    print("="*70)

    print("""
LangChain 提供了多种策略来管理上下文：

1. 消息修剪（Message Trimming）⭐ 推荐
   - 只保留最近 N 条消息
   - 保留系统消息 + 最近对话

2. 消息摘要（Summarization）
   - 定期总结旧消息
   - 用摘要替换历史

3. 滑动窗口（Sliding Window）
   - 固定窗口大小
   - 自动丢弃旧消息

4. Token 限制
   - 根据 Token 数量裁剪
   - 适配不同模型的上下文窗口

这些策略在 phase2_practical/08_context_management 模块中详细讲解！
    """)

if __name__ == "__main__":
    try:
        demo_long_conversation()
        show_solutions()

        print("\n" + "="*70)
        print(" 下一步")
        print("="*70)
        print("\n查看详细解决方案：")
        print("  cd phase2_practical/08_context_management")
        print("  python main.py")

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
