<div align="center">

  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-1.0+-green?logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMiAyTDIgN0wyMCA3TDEyIDEyTTIgN0wxMiAxMkwyMCA3Ii8+PC9zdmc+" alt="LangChain" />
  <img src="https://img.shields.io/badge/LangGraph-0.2+-orange?logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjYiIGN5PSIxMiIgcj0iMyIvPjxjaXJjbGUgY3g9IjE4IiBjeT0iNiIgcj0iMyIvPjxjaXJjbGUgY3g9IjE4IiBjeT0iMTgiIHI9IjMiLz48cGF0aCBkPSJNNiAxMkwxOCA2TTE4IDE4TDYgMTIiLz48L3N2Zz4=" alt="LangGraph" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License" />
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PR Welcome" />

</div>

<h1 align="center">LightFARS: AI 自动研究系统</h1>
<p align="center">
  <b>让 AI 帮你做研究，从文献搜索到论文撰写的全自动化流程</b>
</p>

<p align="center">
  <a href="#-快速开始"><b>快速开始</b></a> •
  <a href="#-演示效果"><b>演示效果</b></a> •
  <a href="#-核心架构"><b>核心架构</b></a> •
  <a href="#-自定义开发"><b>自定义开发</b></a>
</p>

---

## 📖 项目介绍

LightFARS 是一个**完全自动化**的 AI 研究助手。只需输入你想研究的方向，它就会：

1. 🔍 在 arXiv 上搜索相关论文
2. 💡 分析文献并生成研究假设
3. 📋 设计实验并生成代码
4. 🧪 执行实验并分析数据
5. ✍️ 撰写完整的研究论文

**整个过程完全自动化，无需人工干预！**

---

## ✨ 为什么选择 LightFARS？

| 特性 | LightFARS | 其他工具 |
|------|-----------|----------|
| **端到端自动化** | ✅ 从文献到论文全流程 | ❌ 通常只能做一部分 |
| **多 Agent 协作** | ✅ 4 个专业 Agent 配合 | ❌ 单一模型处理 |
| **可视化界面** | ✅ Web UI + CLI 双模式 | ❌ 只有命令行 |
| **多 LLM 支持** | ✅ DeepSeek/OpenAI/Anthropic | ❌ 通常只支持一种 |
| **完全开源** | ✅ MIT 协议，可商用 | ❌ 可能有使用限制 |
| **学习友好** | ✅ 代码清晰，注释完整 | ❌ 复杂难懂 |

---

## 🚀 快速开始

### 第一步：克隆项目

```bash
git clone https://github.com/110376/LightFARS-AI-Research.git
cd LightFARS-AI-Research
```

### 第二步：安装依赖

```bash
pip install -r requirements.txt
```

### 第三步：配置 API Key

创建 `config/.env` 文件：

```bash
# 推荐 DeepSeek（性价比高）
LLM_PROVIDER=openai
LLM_API_KEY=你的API-Key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL_ID=deepseek-chat
```

### 第四步：开始研究

#### 🌐 方式一：Web 界面

```bash
streamlit run web_app.py
```

打开浏览器访问 `http://localhost:8501`

#### ⚡ 方式二：命令行

```bash
# 交互式模式
python start.py -i

# 直接指定主题
python start.py -t "大模型在医疗诊断中的应用"
```

---

## 🎬 演示效果

### 输入

```
研究方向：探索不同 Prompt 策略对 LLM 代码生成质量的影响
```

### 输出

```
projects/你的研究/
├── idea/
│   ├── proposal.md          # 15页研究提案
│   └── plan.json            # 结构化研究计划
├── exp/
│   ├── task_plan.json       # 实验任务分解
│   ├── results/             # 实验数据
│   ├── figures/             # 可视化图表
│   └── analysis.md          # 数据分析报告
└── paper/final/
    ├── report.md            # 完整论文
    └── paper.tex            # LaTeX 格式
```

---

## 🏗️ 核心架构

LightFARS 采用 **多 Agent 协作 + LangGraph 工作流** 架构：

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph 状态机                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   研究方向                                                   │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     │
│  │ Ideation│──▶│ Planning│──▶│Experiment│──▶│ Writing │     │
│  │  Agent  │   │  Agent  │   │  Agent  │   │  Agent  │     │
│  │         │   │         │   │         │   │         │     │
│  │ 💡文献  │   │ 📋任务  │   │ 🧪实验  │   │ ✍️论文  │     │
│  │   搜索  │   │   分解  │   │   执行  │   │   撰写  │     │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘     │
│      │             │              │             │           │
│      ▼             ▼              ▼             ▼           │
│  proposal.md   task_plan.json   results/     report.md      │
│  plan.json                   analysis.md   paper.tex        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| LLM 框架 | LangChain 1.0+ | Agent 和工具管理 |
| 工作流 | LangGraph 0.2+ | 多 Agent 编排 |
| Web 界面 | Streamlit | 可视化操作 |
| 文献搜索 | arXiv API | 论文检索 |

---

## 🧪 自定义开发

### 创建自己的 Agent

```python
# src/agents/my_agent.py

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from src.utils.llm import get_llm

@tool
def my_custom_tool(query: str) -> str:
    """自定义工具"""
    return f"处理结果: {query}"

MY_PROMPT = """你是一位专业的...专家。

你的工作流程：
1. 使用 my_custom_tool 工具
2. 分析结果
3. 生成报告
"""

def create_my_agent():
    llm = get_llm()
    tools = [my_custom_tool]
    llm_with_prompt = llm.bind(system=MY_PROMPT)
    return create_react_agent(llm_with_prompt, tools)
```

### 项目结构

```
LightFARS-AI-Research/
├── src/
│   ├── agents/          # 4个研究 Agent
│   ├── tools/           # 工具定义
│   ├── prompts/         # Prompt 模板
│   ├── workflows/       # LangGraph 工作流
│   └── utils/           # 工具函数
├── start.py             # 命令行启动器
├── web_app.py           # Web 界面
└── config/.env          # API 配置
```

---

## 📚 学习资源

想深入了解 LangChain 和 Agent 开发？推荐按以下顺序学习：

1. **LLM 初始化** → `src/utils/llm.py`
2. **工具定义** → `src/tools/literature.py`
3. **ReAct Agent** → `src/agents/ideation.py`
4. **工作流编排** → `src/workflows/research_flow.py`
5. **Prompt 工程** → `src/prompts/templates.py`

完整的学习文档请查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🛠️ 支持的 LLM

| 提供商 | 推荐场景 | 配置 |
|--------|----------|------|
| **DeepSeek** | 性价比首选，中文优化 | `base_url=https://api.deepseek.com/v1` |
| **OpenAI GPT** | 功能强大，生态完善 | `base_url=https://api.openai.com/v1` |
| **Anthropic Claude** | 长文本处理优秀 | `provider=anthropic` |
| **阿里百炼** | 国内服务稳定 | `base_url=https://dashscope.aliyuncs.com/compatible-mode/v1` |

> 💡 **提示**：不同供应商价格差异较大，建议根据实际需求选择。具体价格请查看各供应商官方网站。

---

## 🤝 参与贡献

欢迎贡献代码！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 👥 Contributors

感谢所有为这个项目做出贡献的人！

<a href="https://github.com/110376/LightFARS-AI-Research/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=110376/LightFARS-AI-Research" />
</a>

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议 - 欢迎商用、修改和分发

---

## 🙏 致谢

- [FARS](https://analemma.ai/fars/) - 项目灵感来源
- [LangChain](https://github.com/langchain-ai/langchain) - 强大的 LLM 框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排框架

---

<div align="center">

  **如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

  **[项目主页](https://github.com/110376/LightFARS-AI-Research) • [问题反馈](https://github.com/110376/LightFARS-AI-Research/issues)**

  <sub>Built with ❤️ by <a href="https://github.com/110376">110376</a></sub>
  <br>
  <sub>让 AI 研究更简单、更高效</sub>

</div>
