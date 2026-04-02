# 模块 17：多 Agent 协作

## 🎯 学习目标

本模块将帮助你理解如何在 LangGraph 中创建多个专业化 Agent，并让它们协作完成复杂任务。

## 📚 核心概念

### 为什么需要多 Agent？

单个 Agent 在处理复杂任务时可能存在以下问题：
- **上下文过载**：单个 Agent 需要处理所有类型的任务
- **专业性不足**：难以在所有领域都表现出色
- **维护困难**：单一庞大的 Agent 难以调试和优化

多 Agent 架构通过**分而治之**的策略解决这些问题。

### 常见的多 Agent 模式

#### 1. 监督者模式（Supervisor Pattern）

```
                    ┌──────────────┐
                    │  Supervisor  │
                    │   (协调者)    │
                    └──────┬───────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  Agent A    │ │  Agent B    │ │  Agent C    │
    │  (研究员)    │ │  (编辑)     │ │  (审核员)   │
    └─────────────┘ └─────────────┘ └─────────────┘
```

- **Supervisor**：接收任务，决定分配给哪个 Agent
- **Worker Agents**：专注于特定类型的任务

#### 2. 协作模式（Collaborative Pattern）

```
    ┌─────────────┐     ┌─────────────┐
    │  Agent A    │────▶│  Agent B    │
    │  (写初稿)    │     │  (审核修改)  │
    └─────────────┘     └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │  Agent C    │
                        │  (最终确认)  │
                        └─────────────┘
```

- Agent 按顺序处理任务
- 每个 Agent 的输出是下一个 Agent 的输入

#### 3. 层级模式（Hierarchical Pattern）

```
                    ┌──────────────┐
                    │   Manager    │
                    └──────┬───────┘
           ┌───────────────┴───────────────┐
           ▼                               ▼
    ┌─────────────┐                 ┌─────────────┐
    │  Team Lead A│                 │  Team Lead B│
    └──────┬──────┘                 └──────┬──────┘
      ┌────┴────┐                     ┌────┴────┐
      ▼         ▼                     ▼         ▼
   Agent 1   Agent 2              Agent 3   Agent 4
```

### 实现多 Agent 的关键组件

```python
from langchain.agents import create_agent
from langgraph.graph import StateGraph

# 1. 定义共享状态
class TeamState(TypedDict):
    task: str
    current_agent: str
    messages: list
    final_result: str

# 2. 创建专业化 Agent
researcher = create_agent(
    model="openai:gpt-4o",
    tools=[search_tool, wikipedia_tool],
    system_prompt="你是一个研究员，专门收集和整理信息。"
)

writer = create_agent(
    model="openai:gpt-4o",
    tools=[],
    system_prompt="你是一个作家，擅长将信息组织成清晰的文章。"
)

# 3. 创建监督者逻辑
def supervisor(state: TeamState) -> str:
    # 决定下一个执行的 Agent
    if "需要研究" in state["task"]:
        return "researcher"
    elif "需要写作" in state["task"]:
        return "writer"
    else:
        return "end"
```

## 🔑 关键 API

### 使用 send() 进行动态分发

```python
from langgraph.types import Send

def supervisor(state: State):
    """将任务分发给多个 Agent"""
    return [
        Send("agent_a", {"task": "子任务1"}),
        Send("agent_b", {"task": "子任务2"})
    ]
```

### Agent 间通信

```python
# 通过状态传递信息
class SharedState(TypedDict):
    messages: Annotated[list, add_messages]
    agent_outputs: dict  # 存储各 Agent 的输出
```

## 📝 本模块示例

### main.py

实现了一个**内容创作团队**：
1. **研究员 Agent**：收集相关信息
2. **作家 Agent**：撰写内容
3. **编辑 Agent**：审核和优化
4. **监督者**：协调整个流程

## 🧪 练习

1. 添加一个"翻译 Agent"，将最终内容翻译成英文
2. 实现并行执行：让研究员和作家同时工作
3. 添加人工审核节点（Human-in-the-loop）

## 📖 延伸阅读

- [LangGraph 多 Agent 教程](https://docs.langchain.com/oss/python/langgraph/tutorials/multi_agent)
- [Agent 协作模式](https://blog.langchain.com/multi-agent-collaboration/)

## ⚠️ 注意事项

1. 合理划分 Agent 职责，避免功能重叠
2. 设置合理的迭代上限，防止无限循环
3. 监控 token 使用，多 Agent 会消耗更多 token
4. 考虑添加错误处理和回退机制
