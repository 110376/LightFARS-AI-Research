"""Experiment Agent（LangChain 1.0+ 正确实现）"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.utils.llm import get_llm
from src.prompts.templates import EXPERIMENT_SYSTEM_PROMPT


def create_experiment_agent(project_dir: str):
    """创建 Experiment Agent（使用 LangGraph 的 create_react_agent）

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

    @tool
    def execute_python_code(code: str) -> str:
        """执行 Python 代码并返回结果。

        参数:
            code: 要执行的 Python 代码

        返回:
            执行结果或错误信息
        """
        # 简单的代码执行（生产环境需要沙箱）
        try:
            # 创建本地命名空间
            local_vars = {}
            exec(code, {}, local_vars)

            # 返回结果
            if "result" in local_vars:
                return str(local_vars["result"])
            else:
                return "代码执行成功（无返回值）"
        except Exception as e:
            return f"错误：{str(e)}"

    tools = [
        read_project_file,
        write_project_file,
        read_project_json,
        write_project_json,
        execute_python_code,
    ]

    # 将系统提示绑定到 LLM
    llm_with_system = llm.bind(system=EXPERIMENT_SYSTEM_PROMPT)

    # 创建 ReAct Agent
    agent = create_react_agent(llm_with_system, tools)

    return agent


def run_experiment_agent(project_dir: str) -> dict:
    """运行 Experiment Agent

    参数:
        project_dir: 项目目录路径

    返回:
        执行结果
    """
    # 创建 Agent
    agent = create_experiment_agent(project_dir)

    # 构造输入
    input_message = HumanMessage(
        content="""
请执行完整的实验过程：

1. 从 exp/task_plan.json 读取任务计划
2. 按顺序执行每个任务：
   - 生成实验代码
   - 执行代码
   - 收集结果
3. 将实验数据保存到 exp/results/ 目录
4. 生成可视化图表到 exp/figures/ 目录
5. 撰写实验分析报告到 exp/analysis.md

注意：
- 每个任务完成后立即更新 task_plan.json 的状态
- 如果任务失败，记录错误并继续下一个任务
- 生成清晰的图表和详细的分析
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
