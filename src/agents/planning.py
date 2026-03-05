"""Planning Agent（LangChain 1.0+ 正确实现）"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.utils.llm import get_llm
from src.prompts.templates import PLANNING_SYSTEM_PROMPT


def create_planning_agent(project_dir: str):
    """创建 Planning Agent（使用 LangGraph 的 create_react_agent）

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

    @tool
    def write_project_json(filepath: str, data: str) -> str:
        """写入 JSON 文件到当前项目目录。"""
        import json

        try:
            parsed = json.loads(data)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            return write_project_file.invoke(
                {"filepath": filepath, "content": formatted}
            )
        except json.JSONDecodeError as e:
            return f"错误：无效的 JSON - {str(e)}"

    tools = [
        read_project_file,
        write_project_file,
        read_project_json,
        write_project_json,
    ]

    # 将系统提示绑定到 LLM
    llm_with_system = llm.bind(system=PLANNING_SYSTEM_PROMPT)

    # 创建 ReAct Agent
    agent = create_react_agent(llm_with_system, tools)

    return agent


def run_planning_agent(project_dir: str) -> dict:
    """运行 Planning Agent

    参数:
        project_dir: 项目目录路径

    返回:
        执行结果
    """
    # 创建 Agent
    agent = create_planning_agent(project_dir)

    # 构造输入
    input_message = HumanMessage(
        content="""
请执行完整的规划过程：

1. 从 idea/proposal.md 读取研究提案
2. 将研究提案拆分为可执行的实验任务
3. 设计实验的评估指标和成功标准
4. 创建任务依赖关系图
5. 将详细的任务计划（JSON 格式）写入 exp/task_plan.json
6. 将实验设计文档写入 exp/experiment_design.md

任务计划应包括：
- 环境配置任务
- 基线实验任务
- 主要实验任务
- 分析任务

每个任务应包含：标题、描述、详细步骤、依赖关系、预期输出。
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
