"""文件操作工具（LangChain 1.0+ 正确实现）"""

from pathlib import Path
import json

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    """读取文件输入参数"""

    filepath: str = Field(description="文件相对路径")
    project_dir: str = Field(description="项目目录路径")


class WriteFileInput(BaseModel):
    """写入文件输入参数"""

    filepath: str = Field(description="文件相对路径")
    content: str = Field(description="要写入的内容")
    project_dir: str = Field(description="项目目录路径")


@tool(args_schema=ReadFileInput)
def read_file(filepath: str, project_dir: str) -> str:
    """读取项目目录中的文件内容。

    参数:
        filepath: 文件相对路径（例如："input/research_directions.md"）
        project_dir: 项目目录的绝对路径或相对路径

    返回:
        文件内容或错误信息
    """
    full_path = Path(project_dir) / filepath

    # 安全检查：防止路径遍历攻击
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


@tool(args_schema=WriteFileInput)
def write_file(filepath: str, content: str, project_dir: str) -> str:
    """写入内容到项目目录中的文件。

    参数:
        filepath: 文件相对路径
        content: 要写入的内容
        project_dir: 项目目录路径

    返回:
        成功消息或错误信息
    """
    full_path = Path(project_dir) / filepath

    # 安全检查
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


class ReadJsonInput(BaseModel):
    """读取 JSON 文件输入参数"""

    filepath: str = Field(description="JSON 文件相对路径")
    project_dir: str = Field(description="项目目录路径")


@tool(args_schema=ReadJsonInput)
def read_json(filepath: str, project_dir: str) -> str:
    """读取并解析 JSON 文件。

    参数:
        filepath: JSON 文件相对路径
        project_dir: 项目目录路径

    返回:
        格式化的 JSON 字符串
    """
    content = read_file.func(filepath=filepath, project_dir=project_dir)

    if content.startswith("错误："):
        return content

    try:
        data = json.loads(content)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"错误：无效的 JSON - {str(e)}"


class WriteJsonInput(BaseModel):
    """写入 JSON 输入参数"""

    filepath: str = Field(description="文件相对路径")
    data: str = Field(description="JSON 字符串")
    project_dir: str = Field(description="项目目录路径")


@tool(args_schema=WriteJsonInput)
def write_json(filepath: str, data: str, project_dir: str) -> str:
    """写入 JSON 数据到文件。

    参数:
        filepath: 文件相对路径
        data: JSON 字符串
        project_dir: 项目目录路径

    返回:
        成功消息或错误信息
    """
    try:
        # 验证并格式化 JSON
        parsed = json.loads(data)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)

        return write_file.func(
            filepath=filepath, content=formatted, project_dir=project_dir
        )
    except json.JSONDecodeError as e:
        return f"错误：无效的 JSON - {str(e)}"
