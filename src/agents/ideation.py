"""Ideation Agent（LangChain 1.0+ 正确实现）"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.utils.llm import get_llm
from src.tools.literature import search_arxiv
from src.tools.file_ops import read_file, write_file, write_json
from src.prompts.templates import IDEATION_SYSTEM_PROMPT


def create_ideation_agent(project_dir: str):
    """创建 Ideation Agent（使用 LangGraph 的 create_react_agent）

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
        """读取当前项目目录中的文件。

        参数:
            filepath: 文件相对路径
        """
        # 直接调用函数，不使用 .func
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
        """写入文件到当前项目目录。

        参数:
            filepath: 文件相对路径
            content: 要写入的内容
        """
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
    def write_project_json(filepath: str, data: str) -> str:
        """写入 JSON 文件到当前项目目录。

        参数:
            filepath: 文件相对路径
            data: JSON 字符串
        """
        import json

        try:
            # 验证并格式化 JSON
            parsed = json.loads(data)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            return write_project_file.invoke(
                {"filepath": filepath, "content": formatted}
            )
        except json.JSONDecodeError as e:
            return f"错误：无效的 JSON - {str(e)}"

    tools = [search_arxiv, read_project_file, write_project_file, write_project_json]

    # 将系统提示绑定到 LLM
    llm_with_system = llm.bind(system=IDEATION_SYSTEM_PROMPT)

    # 创建 ReAct Agent
    agent = create_react_agent(llm_with_system, tools)

    return agent


def run_ideation_agent(project_dir: str) -> dict:
    """运行 Ideation Agent

    参数:
        project_dir: 项目目录路径

    返回:
        执行结果
    """
    # 创建 Agent
    agent = create_ideation_agent(project_dir)

    # 构造输入
    input_message = HumanMessage(
        content="""
请执行完整的构思过程：

1. 从 input/research_directions.md 读取研究方向
2. 在 arXiv 上搜索相关论文（使用 search_arxiv 工具）
3. 分析文献并识别研究空白
4. 生成新颖的研究假设
5. 将完整的研究提案写入 idea/proposal.md
6. 创建结构化的研究计划（JSON）到 idea/plan.json

要全面、学术地完成这个任务。
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
