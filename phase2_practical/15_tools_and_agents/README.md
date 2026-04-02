# 🛠️ 模块 15：工具与 Agent 进阶

> 深入学习工具定义、验证、组合以及 Agent 高级配置

---

## 📚 学习目标

完成本模块后，你将掌握：

1. **高级工具定义** - 使用 Pydantic 进行参数验证
2. **异步工具** - 处理 IO 密集型任务
3. **工具组合** - 构建复杂的工具链
4. **Agent 高级配置** - 自定义行为和错误处理
5. **生产级实践** - 监控、日志、错误恢复

---

## 🔧 核心概念

### 1. 工具定义方式对比

```python
# 方式一：@tool 装饰器（简单场景）
from langchain_core.tools import tool

@tool
def simple_tool(query: str) -> str:
    """简单的工具描述"""
    return f"结果: {query}"

# 方式二：Pydantic 参数模型（推荐，生产级）
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """搜索工具的参数"""
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=10, ge=1, le=100, description="最大结果数")
    language: str = Field(default="zh", description="语言代码")

@tool(args_schema=SearchInput)
def advanced_search(query: str, max_results: int = 10, language: str = "zh") -> str:
    """高级搜索工具，支持参数验证"""
    return f"搜索 '{query}'，返回 {max_results} 条 {language} 结果"

# 方式三：StructuredTool（完全控制）
from langchain_core.tools import StructuredTool

def my_function(x: int, y: int) -> int:
    """计算两数之和"""
    return x + y

structured_tool = StructuredTool.from_function(
    func=my_function,
    name="adder",
    description="计算两个整数的和",
    args_schema=AddInput  # 可选的 Pydantic 模型
)
```

### 2. 异步工具

```python
import asyncio
from langchain_core.tools import tool

@tool
async def async_fetch(url: str) -> str:
    """异步获取网页内容"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 使用异步 Agent
async def main():
    agent = create_agent(model=model, tools=[async_fetch])
    response = await agent.ainvoke({"messages": [...]})
```

### 3. 工具错误处理

```python
@tool
def safe_tool(query: str) -> str:
    """带错误处理的工具"""
    try:
        # 可能失败的操作
        result = risky_operation(query)
        return result
    except ValueError as e:
        return f"参数错误: {e}"
    except Exception as e:
        return f"工具执行失败: {e}"
```

---

## 📁 文件结构

```
15_tools_and_agents/
├── README.md          # 本文件
├── main.py           # 主程序（5个示例）
└── tools/            # 高级工具示例
    ├── __init__.py
    ├── validated_tools.py    # 带验证的工具
    └── async_tools.py        # 异步工具
```

---

## 🚀 运行方式

```bash
cd phase2_practical/15_tools_and_agents
python main.py
```

---

## 📖 示例概览

| 示例 | 主题 | 学习内容 |
|------|------|----------|
| 1 | 参数验证工具 | Pydantic 模型、Field 描述、类型验证 |
| 2 | 错误处理工具 | try/catch、友好错误信息、降级策略 |
| 3 | 工具监控 | 回调函数、执行时间、日志记录 |
| 4 | 工具组合 | 多工具协作、链式调用、结果传递 |
| 5 | 完整 Agent | 生产级配置、多工具、错误恢复 |

---

## 🎯 核心代码示例

### 带验证的工具

```python
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import tool

class EmailInput(BaseModel):
    """邮件发送参数"""
    to: str = Field(description="收件人邮箱")
    subject: str = Field(description="邮件主题")
    body: str = Field(description="邮件正文")

    @field_validator('to')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('无效的邮箱地址')
        return v

@tool(args_schema=EmailInput)
def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件（带参数验证）"""
    # 验证已由 Pydantic 自动完成
    return f"邮件已发送至 {to}"
```

### Agent 回调监控

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain.agents import create_agent

class AgentMonitor(BaseCallbackHandler):
    """监控 Agent 执行"""

    def on_tool_start(self, tool_name, tool_input, **kwargs):
        print(f"🔧 工具开始: {tool_name}")
        print(f"   输入: {tool_input}")

    def on_tool_end(self, output, **kwargs):
        print(f"✅ 工具完成: {output[:100]}...")

agent = create_agent(
    model=model,
    tools=[...],
    # 注意：回调在 invoke 时传入
)

response = agent.invoke(
    {"messages": [...]},
    config={"callbacks": [AgentMonitor()]}
)
```

---

## ❓ 常见问题

### Q1: 何时使用 Pydantic 参数模型？

**A:** 以下场景推荐使用：
- 参数需要类型验证（如邮箱格式、数值范围）
- 参数有复杂的默认值逻辑
- 需要详细的参数描述供 AI 理解
- 生产环境需要严格的输入验证

### Q2: 异步工具 vs 同步工具？

**A:**
- **同步工具**：简单场景，CPU 密集型任务
- **异步工具**：IO 密集型（API 调用、数据库、文件操作）

```python
# 同步
@tool
def sync_tool(x: str) -> str:
    return process(x)

# 异步
@tool
async def async_tool(x: str) -> str:
    return await async_process(x)
```

### Q3: 如何处理工具失败？

**A:** 三层防护：

```python
# 1. 工具内部处理
@tool
def safe_tool(x: str) -> str:
    try:
        return risky_op(x)
    except Exception as e:
        return f"错误: {e}"

# 2. Agent 级重试（使用 prompt）
agent = create_agent(
    model=model,
    tools=[...],
    prompt="如果工具失败，尝试使用其他方法解决问题。"
)

# 3. 调用级重试
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def call_agent(question):
    return agent.invoke({"messages": [{"role": "user", "content": question}]})
```

---

## 🔗 相关模块

- **前置**：04_custom_tools（工具基础）、05_simple_agent（Agent 基础）
- **后续**：16_langgraph_basics（状态图）、17_multi_agent（多 Agent）

---

## 📝 学习检查清单

- [ ] 理解三种工具定义方式的区别
- [ ] 能够使用 Pydantic 进行参数验证
- [ ] 知道何时使用异步工具
- [ ] 掌握工具错误处理策略
- [ ] 能够添加工具监控和日志
- [ ] 理解工具组合的模式

---

**下一步** 👉 `cd ../16_langgraph_basics && python main.py`
