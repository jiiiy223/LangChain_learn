# 模块 18：条件路由

## 🎯 学习目标

掌握 LangGraph 中的条件路由机制，实现动态工作流控制。

## 📚 核心概念

### 什么是条件路由？

条件路由允许你根据**运行时的状态**动态决定下一步执行哪个节点。这是构建智能工作流的关键。

### 路由类型

1. **静态边（Static Edge）**：总是执行固定的下一个节点
2. **条件边（Conditional Edge）**：根据条件函数的返回值选择下一个节点

```python
# 静态边
graph.add_edge("node_a", "node_b")  # 总是 A -> B

# 条件边
graph.add_conditional_edges(
    "node_a",                    # 起始节点
    condition_function,          # 返回下一个节点名的函数
    {"option1": "node_b", "option2": "node_c"}  # 映射
)
```

### 条件函数的写法

```python
from typing import Literal

def my_router(state: MyState) -> Literal["next_a", "next_b", "end"]:
    """路由函数必须返回节点名称"""
    if state["score"] > 80:
        return "next_a"
    elif state["score"] > 50:
        return "next_b"
    else:
        return "end"
```

## 🔑 关键模式

### 1. 循环控制

```python
def should_continue(state) -> Literal["continue", "end"]:
    if state["iteration"] < state["max_iterations"]:
        return "continue"
    return "end"

graph.add_conditional_edges("process", should_continue, {
    "continue": "process",  # 回到自己
    "end": END
})
```

### 2. 错误处理路由

```python
def error_router(state) -> Literal["retry", "fallback", "success"]:
    if state.get("error"):
        if state["retry_count"] < 3:
            return "retry"
        return "fallback"
    return "success"
```

### 3. 多条件组合

```python
def complex_router(state) -> str:
    # 可以组合多个条件
    if state["is_urgent"] and state["has_permission"]:
        return "fast_track"
    elif state["needs_review"]:
        return "review"
    else:
        return "standard"
```

## 📝 本模块示例

实现了：
1. **评分路由**：根据分数选择不同的处理流程
2. **重试机制**：失败时自动重试
3. **复杂决策树**：多条件组合路由

## ⚠️ 注意事项

1. 条件函数必须是**纯函数**，不应有副作用
2. 返回值必须是映射中定义的有效节点名
3. 设置最大迭代次数防止无限循环
