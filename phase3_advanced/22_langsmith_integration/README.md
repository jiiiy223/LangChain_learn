# 模块 22：LangSmith 集成

## 🎯 学习目标

学习如何使用 LangSmith 进行 LLM 应用的追踪、监控和调试。

## 📚 核心概念

### 什么是 LangSmith？

LangSmith 是 LangChain 官方提供的**可观测性平台**，用于：
- 🔍 **追踪**：记录每次 LLM 调用的详细信息
- 📊 **监控**：实时查看应用性能
- 🐛 **调试**：排查问题和优化性能
- 📈 **评估**：系统化测试 LLM 应用

### 核心功能

| 功能 | 描述 |
|------|------|
| Traces | 记录完整的执行链路 |
| Runs | 单次 LLM 调用的详细记录 |
| Feedback | 用户反馈收集 |
| Datasets | 测试数据集管理 |
| Evaluation | 自动化评估 |

## 🔑 配置步骤

### 1. 获取 API Key

1. 访问 [smith.langchain.com](https://smith.langchain.com)
2. 创建账号并获取 API Key
3. 配置环境变量

### 2. 环境变量配置

```bash
# .env 文件
LANGSMITH_API_KEY=your_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=my-project-name
```

### 3. 代码配置

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "my-project"

# LangChain 会自动发送追踪数据
```

## 🔧 追踪示例

### 自动追踪

```python
from langchain.chat_models import init_chat_model

# 启用追踪后，所有调用自动记录
model = init_chat_model("openai:gpt-4o-mini")
response = model.invoke("Hello!")
# -> 自动发送到 LangSmith
```

### 手动标记

```python
from langsmith import traceable

@traceable(name="my_function", tags=["production"])
def my_custom_function(input_data):
    # 你的代码
    return result
```

### 添加元数据

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    metadata={
        "user_id": "user_123",
        "session_id": "sess_456"
    },
    tags=["production", "v2"]
)

response = model.invoke("Hello!", config=config)
```

## 📝 本模块示例

1. **基本追踪**：自动记录 LLM 调用
2. **自定义追踪**：添加自定义元数据和标签
3. **性能监控**：记录延迟和 token 使用
4. **错误追踪**：捕获和记录错误

## ⚠️ 注意事项

1. 生产环境记得设置合适的采样率
2. 敏感数据可能需要脱敏处理
3. 注意 API 调用配额
4. 建议为不同环境使用不同项目
