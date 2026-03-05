# 项目结构说明

## 📁 目录结构

```
lightfars/
├── config/                     # 配置模块
│   ├── .env.example           # 环境变量模板
│   └── settings.py            # Pydantic 配置加载器
│
├── src/                        # 源代码目录
│   ├── __init__.py
│   │
│   ├── agents/                # Agent 实现
│   │   ├── __init__.py
│   │   ├── ideation.py        # 💡 构思 Agent
│   │   ├── planning.py        # 📋 规划 Agent
│   │   ├── experiment.py      # 🧪 实验 Agent
│   │   ├── writing.py         # ✍️ 写作 Agent
│   │   └── news_summarizer.py # 📰 自定义 Agent 示例
│   │
│   ├── tools/                 # 工具定义
│   │   ├── __init__.py
│   │   ├── literature.py      # arXiv 文献搜索工具
│   │   └── file_ops.py        # 文件操作工具
│   │
│   ├── prompts/               # Prompt 模板
│   │   ├── __init__.py
│   │   └── templates.py       # 所有 Agent 的系统提示
│   │
│   ├── workflows/             # LangGraph 工作流
│   │   ├── __init__.py
│   │   └── research_flow.py   # 研究流程状态机
│   │
│   └── utils/                 # 工具函数
│       ├── __init__.py
│       └── llm.py             # LLM 初始化
│
├── projects/                  # 研究项目目录
│   └── prompt-engineering-research/  # 示例研究项目
│       ├── input/             # 输入文件
│       │   └── research_directions.md
│       ├── idea/              # 构思阶段输出
│       │   ├── proposal.md
│       │   ├── plan.json
│       │   └── references/
│       ├── exp/               # 实验阶段输出
│       │   ├── task_plan.json
│       │   ├── experiment_design.md
│       │   ├── results/
│       │   ├── figures/
│       │   └── analysis.md
│       └── paper/             # 写作阶段输出
│           └── final/
│               ├── report.md
│               └── paper.tex
│
├── docs/                      # 文档资源
│   ├── 论文1.png
│   ├── 论文2.png
│   └── 论文3.png
│
├── start.py                   # ⚡ 简易启动器
├── web_app.py                 # 🌐 Web 界面
├── main.py                    # 主入口
├── run_research.py            # 命令行运行器
├── test_news_agent.py         # 自定义 Agent 测试
├── requirements.txt           # 依赖列表
├── .gitignore                 # Git 忽略配置
├── LICENSE                    # MIT 许可证
├── README.md                  # 项目说明
├── README-zh_CN.md            # 中文说明
├── CONTRIBUTING.md            # 贡献指南
└── PROJECT_STRUCTURE.md       # 本文件
```

---

## 🧩 核心模块说明

### 1. Agent 模块 (`src/agents/`)

每个 Agent 负责研究流程的一个阶段：

| 文件 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `ideation.py` | 文献搜索、假设生成 | 研究方向 | proposal.md, plan.json |
| `planning.py` | 任务分解、实验设计 | proposal.md | task_plan.json |
| `experiment.py` | 代码生成、实验执行 | task_plan.json | results/, analysis.md |
| `writing.py` | 论文撰写 | 所有阶段输出 | report.md, paper.tex |

**Agent 创建模式**：

```python
def create_xxx_agent(project_dir: str):
    # 1. 获取 LLM
    llm = get_llm()

    # 2. 定义工具（可选绑定 project_dir）
    tools = [...]

    # 3. 绑定系统提示
    llm_with_system = llm.bind(system=XXX_SYSTEM_PROMPT)

    # 4. 创建 ReAct Agent
    agent = create_react_agent(llm_with_system, tools)

    return agent
```

---

### 2. 工具模块 (`src/tools/`)

工具是 Agent 可以调用的函数。

**工具定义模式**：

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    """输入参数定义"""
    param: str = Field(description="参数说明")

@tool(args_schema=ToolInput)
def my_tool(param: str) -> str:
    """工具描述（会被 LLM 看到）

    Args:
        param: 参数说明

    Returns:
        返回值说明
    """
    # 实现代码
    return result
```

**现有工具**：

| 文件 | 工具 | 功能 |
|------|------|------|
| `literature.py` | `search_arxiv` | 搜索 arXiv 论文 |
| `file_ops.py` | `read_file` | 读取文件 |
| `file_ops.py` | `write_file` | 写入文件 |
| `file_ops.py` | `read_json` | 读取 JSON |
| `file_ops.py` | `write_json` | 写入 JSON |

---

### 3. Prompt 模块 (`src/prompts/`)

包含所有 Agent 的系统提示词。

**Prompt 结构**：

```
┌─────────────────────────────────────────────────────────────┐
│  第1层：角色定义 (Identity)                                  │
│  "你是一位专业的 AI 研究专家"                               │
├─────────────────────────────────────────────────────────────┤
│  第2层：能力说明 (Capabilities)                              │
│  "- 在 arXiv 上搜索学术论文"                                │
│  "- 读取和写入项目目录中的文件"                            │
├─────────────────────────────────────────────────────────────┤
│  第3层：工作流程 (Workflow)                                 │
│  "1. 从 input/ 读取研究方向"                               │
│  "2. 在 arXiv 上搜索相关论文"                              │
│  "3. 分析文献并识别研究空白"                               │
├─────────────────────────────────────────────────────────────┤
│  第4层：输出要求 (Requirements)                             │
│  "要全面、学术、创新"                                       │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. 工作流模块 (`src/workflows/`)

使用 LangGraph StateGraph 编排多 Agent 协作。

**StateGraph 结构**：

```
┌─────────────────────────────────────────────────────────────┐
│                    StateGraph 状态机                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐│
│   │Ideation │───▶│Planning │───▶│Experiment│───▶│ Writing ││
│   │  Node   │    │  Node   │    │  Node   │    │  Node   ││
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘│
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │              ResearchState (状态)                   │  │
│   │  - project_dir: str                                 │  │
│   │  - research_directions: str                         │  │
│   │  - current_stage: str                               │  │
│   │  - completed_agents: List[str]                      │  │
│   │  - messages: List[str]                              │  │
│   │  - error: str                                       │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 5. 工具模块 (`src/utils/`)

通用工具函数。

**LLM 初始化**：

```python
def get_llm():
    """获取 LLM 实例（基于配置）"""
    return ChatOpenAI(
        model=settings.llm_model_id,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
    )
```

支持通过 `config/.env` 切换不同 LLM 提供商。

---

## 🚀 启动脚本

| 脚本 | 功能 | 使用方式 |
|------|------|----------|
| `start.py` | 交互式启动器 | `python start.py -i` |
| `web_app.py` | Web 界面 | `streamlit run web_app.py` |
| `main.py` | 主入口 | `python main.py` |
| `run_research.py` | 命令行运行 | `python run_research.py my-project` |

---

## 📊 数据流

```
用户输入研究方向
       ↓
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph StateGraph                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │  Ideation   │───▶│  Planning   │───▶│  Experiment  │    │
│  │   Agent     │    │   Agent     │    │   Agent     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                   │                   │            │
│        ▼                   ▼                   ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │ proposal.md │    │task_plan.json│    │  results/   │    │
│  │  plan.json  │    │             │    │ analysis.md │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                                             │              │
│                                             ▼              │
│                                      ┌─────────────┐     │
│                                      │  Writing    │     │
│                                      │   Agent     │     │
│                                      └─────────────┘     │
│                                             │              │
│                                             ▼              │
│                                      ┌─────────────┐     │
│                                      │ report.md   │     │
│                                      │  paper.tex  │     │
│                                      └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 扩展指南

### 添加新 Agent

1. 在 `src/agents/` 创建新文件
2. 参照 `ideation.py` 的模式实现
3. 在 `research_flow.py` 中添加节点
4. 更新工作流图

### 添加新工具

1. 在 `src/tools/` 创建新文件
2. 使用 `@tool` 装饰器定义
3. 在 Agent 中引用

### 修改 Prompt

1. 编辑 `src/prompts/templates.py`
2. 保持四层结构
3. 测试效果

---

希望这份文档能帮助你快速理解 LightFARS 的项目结构！
