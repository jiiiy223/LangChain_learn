# 第三阶段：高级主题 (Advanced Topics)

## 📋 概述

本阶段涵盖 LangChain 1.0 和 LangGraph 的高级特性，包括复杂工作流构建、多智能体系统、多模态处理和生产级集成。

## 🎯 学习目标

完成本阶段后，你将能够：
- 使用 LangGraph 构建复杂的状态机工作流
- 设计和实现多智能体协作系统
- 处理多模态输入（文本、图像、文件）
- 集成 LangSmith 进行监控和调试
- 实现生产级的错误处理和容错机制

## 📚 模块列表

### 核心模块

| 模块 | 名称 | 描述 | 难度 |
|------|------|------|------|
| 16 | [LangGraph 基础](./16_langgraph_basics/) | 状态图、节点、边和检查点 | ⭐⭐⭐ |
| 17 | [多智能体系统](./17_multi_agent/) | Supervisor模式、协作和调度 | ⭐⭐⭐⭐ |
| 18 | [条件路由](./18_conditional_routing/) | 动态分支、重试和决策树 | ⭐⭐⭐ |

### 多模态处理

| 模块 | 名称 | 描述 | 难度 |
|------|------|------|------|
| 19 | [图像输入处理](./19_image_input/) | 视觉理解、OCR、图表分析 | ⭐⭐⭐ |
| 20 | [文件处理](./20_file_handling/) | 文档加载、分块、多格式支持 | ⭐⭐ |
| 21 | [混合模态](./21_mixed_modality/) | 文本+图像+数据的综合处理 | ⭐⭐⭐⭐ |

### 生产集成

| 模块 | 名称 | 描述 | 难度 |
|------|------|------|------|
| 22 | [LangSmith 集成](./22_langsmith_integration/) | 追踪、监控、性能分析 | ⭐⭐⭐ |
| 23 | [错误处理](./23_error_handling/) | 重试、降级、容错机制 | ⭐⭐⭐ |

## 🛠️ 技术栈

- **LangChain 1.0**: 核心框架
- **LangGraph**: 状态机工作流
- **OpenAI GPT-4o-mini**: 默认模型
- **LangSmith**: 可观测性平台
- **Pydantic**: 数据验证

## 📦 安装依赖

```bash
pip install langchain langchain-openai langgraph langsmith python-dotenv pydantic
```

## 🔧 环境配置

```bash
# .env 文件
OPENAI_API_KEY=your-api-key

# LangSmith（可选）
LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=langchain-study
```

## 📖 学习路径

```
16_langgraph_basics
        │
        ▼
17_multi_agent ◄──── 18_conditional_routing
        │
        ▼
19_image_input ──► 20_file_handling ──► 21_mixed_modality
                                               │
                                               ▼
                        22_langsmith_integration
                                               │
                                               ▼
                          23_error_handling
```

## 💡 核心概念

### LangGraph 状态机

```python
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: Annotated[list, add_messages]
    status: str

graph = StateGraph(State)
graph.add_node("process", process_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)
```

### 多智能体协作

```python
# Supervisor 模式
def supervisor(state):
    # 分析任务并分配给专业智能体
    return {"next": "worker_1"}

# 条件路由
graph.add_conditional_edges(
    "supervisor",
    route_function,
    {"worker_1": "w1", "worker_2": "w2"}
)
```

### 错误处理

```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def call_with_retry():
    return model.invoke(messages)
```

## 🎓 先决条件

- 完成第一阶段（基础知识）
- 完成第二阶段（中级主题）
- Python 异步编程基础
- 对状态机有基本了解

## 📝 练习建议

1. **循序渐进**: 按模块顺序学习
2. **动手实践**: 运行所有示例代码
3. **修改实验**: 尝试修改参数观察效果
4. **结合项目**: 思考如何应用到实际项目

## 🔗 下一步

完成本阶段后，继续学习 [第四阶段：综合项目](../phase4_projects/)，将所学知识整合到完整的应用中。
