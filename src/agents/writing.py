"""Writing Agent（LangChain 1.0+ 正确实现）"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.utils.llm import get_llm
from src.prompts.templates import WRITING_SYSTEM_PROMPT


def create_writing_agent(project_dir: str):
    """创建 Writing Agent（使用 LangGraph 的 create_react_agent）

    参数:
        project_dir: 项目目录路径

    返回:
        LangGraph ReAct Agent
    """
    # 获取 LLM
    llm = get_llm()

    # 定义工具（绑定 project_dir）
    @tool
    def read_project_file(filepath: str) -> str:
        """读取当前项目目录中的文件。"""
        from pathlib import Path

        full_path = Path(project_dir) / filepath

        try:
            full_path = full_path.resolve()
            project_path = Path(project_dir).resolve()

            if not str(full_path).startswith(str(project_path)):
                return "错误：无效路径（超出项目目录）"

            if not full_path.exists():
                return f"错误：文件不存在：{filepath}"

            return full_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"错误：{str(e)}"

    @tool
    def write_project_file(filepath: str, content: str) -> str:
        """写入文件到当前项目目录。"""
        from pathlib import Path

        full_path = Path(project_dir) / filepath

        try:
            full_path = full_path.resolve()
            project_path = Path(project_dir).resolve()

            if not str(full_path).startswith(str(project_path)):
                return "错误：无效路径（超出项目目录）"

            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")

            return f"成功写入到 {filepath}"
        except Exception as e:
            return f"错误：{str(e)}"

    @tool
    def read_project_json(filepath: str) -> str:
        """读取当前项目目录中的 JSON 文件。"""
        import json

        content = read_project_file.invoke({"filepath": filepath})

        if content.startswith("错误："):
            return content

        try:
            data = json.loads(content)
            return json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            return f"错误：无效的 JSON - {str(e)}"

    tools = [read_project_file, write_project_file, read_project_json]

    # 将系统提示绑定到 LLM
    llm_with_system = llm.bind(system=WRITING_SYSTEM_PROMPT)

    # 创建 ReAct Agent
    agent = create_react_agent(llm_with_system, tools)

    return agent


def run_writing_agent(project_dir: str) -> dict:
    """运行 Writing Agent

    参数:
        project_dir: 项目目录路径

    返回:
        执行结果
    """
    # 创建 Agent
    agent = create_writing_agent(project_dir)

    # 构造输入
    input_message = HumanMessage(
        content="""
请执行完整的论文撰写过程：

1. 从 idea/proposal.md 读取研究提案
2. 从 exp/results/ 目录读取所有实验结果
3. 从 exp/analysis.md 读取实验分析
4. 撰写完整的研究论文，包括：
   - 标题和摘要
   - 引言（背景、动机、贡献）
   - 相关工作（文献综述）
   - 方法（实验设计）
   - 实验（设置、结果）
   - 分析（对比、讨论）
   - 结论（总结、未来工作）
   - 参考文献
5. 将 Markdown 格式的论文保存到 paper/final/report.md
6. （可选）将 LaTeX 格式的论文保存到 paper/final/paper.tex

要求：
- 论文要结构清晰、逻辑严谨
- 图表引用要准确
- 参考文献要完整
- 语言要学术化
"""
    )

    # 执行 Agent
    result = agent.invoke({"messages": [input_message]})

    # 提取最终消息
    final_message = result["messages"][-1]

    return {
        "status": "success",
        "final_message": final_message.content,
        "all_messages": [msg.content for msg in result["messages"]],
    }
