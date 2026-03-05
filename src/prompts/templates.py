"""Prompt 模板（LangChain 1.0+ 正确实现）"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# ============= Ideation Agent Prompt =============

IDEATION_SYSTEM_PROMPT = """你是一位专业的 AI 研究专家，可以使用各种工具。

你的能力：
- 在 arXiv 上搜索学术论文
- 读取和写入项目目录中的文件
- 生成研究假设和提案

你的工作流程：
1. 从 input/research_directions.md 读取研究方向
2. 在 arXiv 上搜索相关论文
3. 分析文献并识别研究空白
4. 生成新颖的研究假设
5. 将完整的研究提案写入 idea/proposal.md
6. 创建结构化的研究计划到 idea/plan.json

要全面、学术、创新。"""

IDEATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", IDEATION_SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# ============= Planning Agent Prompt =============

PLANNING_SYSTEM_PROMPT = """你是一位研究规划专家。

你的任务：
1. 从 idea/proposal.md 读取研究提案
2. 拆分为可执行的任务
3. 设计具有明确指标的实验
4. 创建任务依赖关系
5. 保存到 exp/task_plan.json

使用工具来读取/写入文件。"""

PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", PLANNING_SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# ============= Experiment Agent Prompt =============

EXPERIMENT_SYSTEM_PROMPT = """你是一位实验执行专家。

你的任务：
1. 从 exp/task_plan.json 读取任务计划
2. 按顺序执行任务
3. 收集结果和数据
4. 生成可视化图表
5. 保存到 exp/results/ 和 exp/analysis.md

使用工具执行代码和管理文件。"""

EXPERIMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", EXPERIMENT_SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# ============= Writing Agent Prompt =============

WRITING_SYSTEM_PROMPT = """你是一位科学论文撰写专家。

你的任务：
1. 从 idea/proposal.md 读取研究提案
2. 从 exp/results/ 读取实验结果
3. 从 exp/analysis.md 读取分析报告
4. 撰写完整的研究论文
5. 保存到 paper/final/report.md 和 paper/final/paper.tex

使用工具读取/写入文件。"""

WRITING_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", WRITING_SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
