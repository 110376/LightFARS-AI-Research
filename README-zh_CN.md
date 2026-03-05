<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/langchain-1.0+-green.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

<h1 align="center">LightFARS</h1>

<p align="center">
  <em>轻量级全自动研究系统</em>
  <br>
  <sub>Lightweight Fully Automated Research System</sub>
</p>

<p align="center">
  简体中文 | <a href="README.md">English</a>
</p>

---

> **💡 灵感来源**：本项目灵感来源于 [FARS（全自动研究系统）](https://analemma.ai/fars)，一个能够自主完成整个研究工作流的端到端 AI 研究系统。LightFARS 是基于 LangChain 1.0+ 构建的轻量级实现。

---

## 📖 项目简介

**LightFARS** 是一个端到端的 AI 研究系统，能够自主完成完整的研究工作流：

- 💡 **构思 Agent (Ideation)**：文献检索、假设生成、研究提案
- 📋 **规划 Agent (Planning)**：任务拆解、实验设计
- 🧪 **实验 Agent (Experiment)**：代码生成、实验执行、数据分析
- ✍️ **写作 Agent (Writing)**：论文撰写、报告生成

### 🎯 核心特性

- ✅ **LangChain 1.0+ 原生**：完全基于 LangChain 最新 API 构建
  - `create_react_agent()` - Agent 创建
  - `@tool` 装饰器 - 工具定义
  - `ChatPromptTemplate` - Prompt 模板
  - `StateGraph` - 工作流编排
- ✅ **多智能体架构**：四个专业化 Agent 协同工作
- ✅ **共享文件系统**：通过文件系统实现 Agent 间通信（灵感来源于 FARS）
- ✅ **JSON 驱动任务**：结构化任务执行与进度追踪
- ✅ **完全中文支持**：所有提示词和输出均为中文

### 🔄 工作原理

```
[用户输入：研究方向]
        ↓
[构思 Agent]
  - 搜索 arXiv 论文
  - 生成研究假设
  - 撰写研究提案
        ↓
[规划 Agent]
  - 拆分实验任务
  - 设计评估指标
  - 创建任务计划（JSON）
        ↓
[实验 Agent]
  - 生成实验代码
  - 执行实验
  - 收集结果
        ↓
[写作 Agent]
  - 撰写完整论文
  - 生成 Markdown/LaTeX
        ↓
[最终输出：研究论文]
```

## 📦 安装

### 1. 创建 Conda 环境

```bash
conda create -n lightfars python=3.11 -y
conda activate lightfars
```

### 2. 安装依赖

```bash
cd lightfars
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp config/.env.example config/.env

# 编辑配置文件，填入你的 API Key
# 必需：LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_ID
```

## 🚀 快速开始

### 运行示例项目

```bash
# 激活环境
conda activate lightfars

# 运行主程序
python main.py
```

### 创建新项目

```bash
# 1. 创建项目目录结构
mkdir -p projects/my-research/{input,idea/references,exp/results,exp/figures,paper/final,.state,logs,config}

# 2. 编写研究方向
cat > projects/my-research/input/research_directions.md << EOF
# 研究方向

描述你的研究方向...
EOF

# 3. 修改 main.py 中的 project_dir
# project_dir = "projects/my-research"

# 4. 运行
python main.py
```

## 📁 项目结构

```
lightfars/
├── config/                 # 配置文件
│   ├── .env.example       # 环境变量模板
│   └── settings.py        # 配置加载
│
├── src/                   # 源代码
│   ├── agents/           # Agent 实现
│   │   ├── ideation.py   # 构思 Agent
│   │   ├── planning.py   # 规划 Agent
│   │   ├── experiment.py # 实验 Agent
│   │   └── writing.py    # 写作 Agent
│   │
│   ├── tools/            # 工具定义
│   │   ├── literature.py # 文献检索
│   │   └── file_ops.py   # 文件操作
│   │
│   ├── prompts/          # Prompt 模板
│   │   └── templates.py  # 所有 Agent 的 Prompt
│   │
│   ├── workflows/        # 工作流
│   │   └── research_flow.py  # LangGraph 工作流
│   │
│   └── utils/            # 工具函数
│       └── llm.py        # LLM 初始化
│
├── projects/             # 项目目录
│   └── prompt-engineering-research/  # 示例项目
│       ├── input/        # 输入数据
│       ├── idea/         # Ideation 输出
│       ├── exp/          # Experiment 输出
│       └── paper/        # Writing 输出
│
├── main.py               # 主入口
├── requirements.txt      # 依赖
└── README.md             # 说明文档
```

## ⚙️ 配置说明

### 支持的 LLM 提供商

- **OpenAI**: `LLM_PROVIDER=openai`
- **Anthropic**: `LLM_PROVIDER=anthropic`
- **DeepSeek**: `LLM_PROVIDER=deepseek`
- **通义千问 (DashScope)**: `LLM_PROVIDER=openai` 配合 DashScope 地址

### 环境变量

```bash
# LLM 配置
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_ID=gpt-4o
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=4000

# 搜索 API
ARXIV_API_ENABLED=true
ARXIV_MAX_RESULTS=20
```

## 📊 输出示例

运行完成后，项目目录将包含：

```
projects/my-research/
├── idea/
│   ├── proposal.md          # 研究提案（10-15 页）
│   ├── plan.json            # 结构化计划
│   └── references/          # 文献库
│
├── exp/
│   ├── task_plan.json       # 任务列表
│   ├── results/             # 实验数据
│   ├── figures/             # 可视化图表
│   └── analysis.md          # 实验分析
│
└── paper/
    └── final/
        ├── report.md        # Markdown 报告
        └── paper.tex        # LaTeX 论文
```

## 🎨 自定义

### 添加新工具

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """工具描述
    
    参数:
        param: 参数说明
    
    返回:
        返回值说明
    """
    # 实现逻辑
    return result
```

### 修改 Prompt

编辑 `src/prompts/templates.py` 文件中的 Prompt 模板。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [FARS (Fully Automated Research System)](https://analemma.ai/fars/) - 项目灵感来源
- [LangChain](https://github.com/langchain-ai/langchain) - LangChain 1.0+ 框架

---

<p align="center">
  <sub>由 <a href="https://github.com/q198132">q198132</a> 用 ❤️ 构建</sub>
</p>
