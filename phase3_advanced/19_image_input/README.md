# 模块 19：图像输入

## 🎯 学习目标

学习如何使用视觉模型（Vision Models）处理图像输入，实现多模态 AI 应用。

## 📚 核心概念

### 多模态支持

LangChain 1.0 原生支持多模态输入：
- **文本**：传统的文字输入
- **图像**：照片、截图、图表等
- **文件**：PDF、文档等

### 支持视觉的模型

| 模型 | 图像支持 | 特点 |
|------|----------|------|
| GPT-4o | ✅ | 强大的多模态理解 |
| GPT-4o-mini | ✅ | 性价比高 |
| Claude 3.5 | ✅ | 出色的图像理解 |
| Gemini Pro | ✅ | Google 的多模态模型 |

### 图像输入方式

```python
from langchain_core.messages import HumanMessage

# 方式 1：URL
message = HumanMessage(content=[
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
])

# 方式 2：Base64 编码
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = HumanMessage(content=[
    {"type": "text", "text": "这是什么？"},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
])
```

## 🔑 关键 API

### 使用 init_chat_model

```python
from langchain.chat_models import init_chat_model

# 初始化支持视觉的模型
model = init_chat_model("openai:gpt-4o")

# 发送带图像的消息
response = model.invoke([message_with_image])
```

### 图像处理工具

```python
from langchain_core.tools import tool
import base64

@tool
def analyze_image(image_path: str) -> str:
    """分析图像并返回描述"""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()
    
    message = HumanMessage(content=[
        {"type": "text", "text": "详细描述这张图片"},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
    ])
    
    return model.invoke([message]).content
```

## 📝 本模块示例

1. **图像描述**：让模型描述图片内容
2. **图像问答**：基于图片回答问题
3. **OCR 文字识别**：从图像中提取文字
4. **图表分析**：理解图表数据

## ⚠️ 注意事项

1. 图像大小有限制，建议压缩大图片
2. Base64 编码会增加 payload 大小约 33%
3. 不同模型的图像理解能力差异较大
4. 注意 token 消耗，图像会消耗较多 token
