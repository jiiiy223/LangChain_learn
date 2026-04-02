# 模块 20：文件处理

## 🎯 学习目标

学习如何在 LangChain 中处理各种文件类型，包括文档加载、解析和分析。

## 📚 核心概念

### 支持的文件类型

| 类型 | 扩展名 | 加载器 |
|------|--------|--------|
| PDF | .pdf | PyPDFLoader |
| Word | .docx | Docx2txtLoader |
| 文本 | .txt | TextLoader |
| Markdown | .md | UnstructuredMarkdownLoader |
| CSV | .csv | CSVLoader |
| JSON | .json | JSONLoader |
| HTML | .html | BSHTMLLoader |

### 文档加载器基础

```python
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 加载 PDF
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 加载文本文件
loader = TextLoader("file.txt", encoding="utf-8")
documents = loader.load()
```

### 文档结构

```python
from langchain_core.documents import Document

# 每个文档包含
doc = Document(
    page_content="文档内容...",  # 实际文本
    metadata={                    # 元数据
        "source": "file.pdf",
        "page": 1
    }
)
```

## 🔑 关键 API

### 文本分割

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 每块最大字符数
    chunk_overlap=200,    # 块之间重叠字符数
    separators=["\n\n", "\n", "。", " "]  # 分割优先级
)

chunks = splitter.split_documents(documents)
```

### 目录加载

```python
from langchain_community.document_loaders import DirectoryLoader

# 加载目录下所有 txt 文件
loader = DirectoryLoader(
    "data/",
    glob="**/*.txt",      # 匹配模式
    loader_cls=TextLoader
)
documents = loader.load()
```

## 📝 本模块示例

1. **单文件加载**：加载和解析单个文件
2. **批量加载**：处理目录中的多个文件
3. **智能分割**：将长文档分割成适合处理的块
4. **文档问答**：基于文档内容回答问题

## ⚠️ 注意事项

1. 大文件需要分块处理以避免超出 token 限制
2. PDF 解析质量取决于 PDF 的结构
3. 注意文件编码，中文文件建议使用 UTF-8
4. 某些加载器需要额外安装依赖
