<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/langchain-1.0+-green.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/langgraph-0.2+-orange.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

<h1 align="center">LightFARS</h1>

<p align="center">
  <em>Lightweight Fully Automated Research System</em>
  <br>
  <sub>轻量级全自动 AI 研究系统</sub>
</p>

<p align="center">
  <a href="#-快速开始">快速开始</a> •
  <a href="#-核心功能">核心功能</a> •
  <a href="#-使用方式">使用方式</a> •
  <a href="#-学习资源">学习资源</a>
</p>

---

> **💡 灵感来源**: 本项目受 [FARS (Fully Automated Research System)](https://analemma.ai/fars) 启发，是一个使用 LangChain 1.0+ 和 LangGraph 构建的轻量级 AI 研究自动化系统。

---

## 📖 项目简介

**LightFARS** 是一个端到端的 AI 研究系统，能够自动完成从文献检索到论文撰写的完整研究流程：

| Agent | 功能 |
|-------|------|
| 💡 **Ideation Agent** | 文献搜索、假设生成、研究提案 |
| 📋 **Planning Agent** | 任务分解、实验设计、JSON 计划 |
| 🧪 **Experiment Agent** | 代码生成、实验执行、数据分析 |
| ✍️ **Writing Agent** | 论文撰写、Markdown/LaTeX 输出 |

### 🎯 核心特性

- ✅ **LangChain 1.0+ 原生**: 使用最新 LangChain API 构建
- ✅ **LangGraph 工作流**: StateGraph 状态机编排多 Agent 协作
- ✅ **ReAct Agent**: 推理+行动的智能代理
- ✅ **多 LLM 支持**: OpenAI / DeepSeek / Anthropic / Qwen
- ✅ **Web 界面**: Streamlit 可视化操作
- ✅ **一键启动**: 命令行交互式启动器
- ✅ **完全中文化**: 所有 Prompt 和输出支持中文

### 🔄 工作流程

```
[输入研究方向]
       ↓
┌──────────────┐
│  Ideation    │ → 文献搜索 → 假设生成 → 研究提案
└──────────────┘
       ↓
┌──────────────┐
│  Planning    │ → 任务分解 → 实验设计 → JSON计划
└──────────────┘
       ↓
┌──────────────┐
│  Experiment  │ → 代码生成 → 实验执行 → 数据分析
└──────────────┘
       ↓
┌──────────────┐
│  Writing     │ → 论文撰写 → 格式转换 → 最终输出
└──────────────┘
       ↓
[完整研究论文]
```

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
# 克隆项目
git clone https://github.com/你的用户名/lightfars.git
cd lightfars

# 安装依赖
pip install -r requirements.txt
```

### 2️⃣ 配置 API

复制 `config/.env.example` 为 `config/.env`，填入你的 API Key：

```bash
# 使用 DeepSeek（推荐，便宜）
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-deepseek-key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL_ID=deepseek-chat

# 或使用 OpenAI
# LLM_PROVIDER=openai
# LLM_API_KEY=sk-your-openai-key
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL_ID=gpt-4o
```

### 3️⃣ 开始使用

#### 🌟 方式一：Web 界面（推荐）

```bash
streamlit run web_app.py
```

浏览器访问 `http://localhost:8501`

#### ⚡ 方式二：交互式命令

```bash
python start.py -i
```

#### 📝 方式三：直接指定主题

```bash
python start.py -t "AI 在教育领域的应用"
```

---

## 🎨 使用方式

### Web 界面

```
┌─────────────────────────────────────────────────────────────┐
│         🔬 LightFARS - 全自动研究系统                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📝 研究主题                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [AI 教育应用 ▼]                                    │   │
│  │                                                     │   │
│  │ 探索人工智能在教育领域的应用...                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🚀 开始研究                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              🔥 开始研究                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 命令行启动器

```bash
# 交互式模式
python start.py -i

# 直接指定主题和项目名
python start.py -p 我的研究 -t "大模型在医疗诊断中的应用"

# 查看帮助
python start.py --help
```

---

## 📁 项目结构

```
lightfars/
├── config/                 # 配置文件
│   ├── .env.example       # 环境变量模板
│   └── settings.py        # 配置加载器
│
├── src/                   # 源代码
│   ├── agents/           # Agent 实现
│   │   ├── ideation.py   # 构思 Agent
│   │   ├── planning.py   # 规划 Agent
│   │   ├── experiment.py # 实验 Agent
│   │   ├── writing.py    # 写作 Agent
│   │   └── news_summarizer.py  # 自定义 Agent 示例
│   │
│   ├── tools/            # 工具定义
│   │   ├── literature.py # arXiv 文献搜索
│   │   └── file_ops.py   # 文件操作工具
│   │
│   ├── prompts/          # Prompt 模板
│   │   └── templates.py  # 所有 Agent 的提示词
│   │
│   ├── workflows/        # LangGraph 工作流
│   │   └── research_flow.py  # 研究流程状态机
│   │
│   └── utils/            # 工具函数
│       └── llm.py        # LLM 初始化
│
├── projects/             # 研究项目目录
│   ├── prompt-engineering-research/  # 示例项目
│   └── news-reports/     # 新闻报告示例
│
├── start.py              # 简易启动器
├── web_app.py            # Web 界面
├── main.py               # 主入口
└── requirements.txt      # 依赖列表
```

---

## 📊 输出结果

运行完成后，项目目录包含：

```
projects/你的研究/
├── idea/
│   ├── proposal.md          # 研究提案 (10-15页)
│   └── plan.json            # 研究计划
│
├── exp/
│   ├── task_plan.json       # 实验任务
│   ├── results/             # 实验结果
│   ├── figures/             # 可视化图表
│   └── analysis.md          # 分析报告
│
└── paper/final/
    ├── report.md            # Markdown 报告
    └── paper.tex            # LaTeX 论文
```

---

## 🧪 自定义 Agent

参考 `src/agents/news_summarizer.py` 创建自己的 Agent：

```python
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from src.utils.llm import get_llm

@tool
def my_tool(param: str) -> str:
    """工具描述"""
    return f"结果: {param}"

MY_SYSTEM_PROMPT = """你是一位 [角色]...
你的能力：...
你的工作流程：1. ... 2. ... 3. ...
"""

def create_my_agent():
    llm = get_llm()
    tools = [my_tool, ...]
    llm_with_system = llm.bind(system=MY_SYSTEM_PROMPT)
    return create_react_agent(llm_with_system, tools)
```

---

## 📚 学习资源

| 主题 | 文件 |
|------|------|
| LangChain 基础 | `src/utils/llm.py`, `src/tools/` |
| ReAct Agent | `src/agents/ideation.py` |
| LangGraph 工作流 | `src/workflows/research_flow.py` |
| Prompt 工程 | `src/prompts/templates.py` |
| 自定义 Agent | `src/agents/news_summarizer.py` |

---

## 🛠️ 技术栈

- **Python 3.11+**
- **LangChain 1.0+** - LLM 应用框架
- **LangGraph 0.2+** - 工作流编排
- **Streamlit** - Web 界面
- **arXiv API** - 文献搜索

---

## ⚙️ 配置说明

### 支持的 LLM 提供商

| 提供商 | LLM_PROVIDER | LLM_BASE_URL |
|--------|-------------|-------------|
| OpenAI | `openai` | `https://api.openai.com/v1` |
| DeepSeek | `openai` | `https://api.deepseek.com/v1` |
| Anthropic | `anthropic` | `https://api.anthropic.com` |
| 阿里百炼 | `openai` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

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

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [FARS](https://analemma.ai/fars/) - 项目灵感来源
- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排框架

---

## 📮 联系方式

- 项目主页: [https://github.com/你的用户名/lightfars](https://github.com/你的用户名/lightfars)
- 问题反馈: [Issues](https://github.com/你的用户名/lightfars/issues)

---

<p align="center">
  <sub>Built with ❤️ by LightFARS Community</sub>
  <br>
  <sub>让 AI 研究更简单</sub>
</p>
