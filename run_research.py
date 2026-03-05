"""LightFARS 研究运行器 - 支持命令行参数"""

import sys
import io
import argparse
from pathlib import Path
from src.workflows.research_flow import create_research_app

# Fix Windows terminal encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_research(project_name: str, research_topic: str = None):
    """运行研究项目

    Args:
        project_name: 项目目录名称 (如: my-research)
        research_topic: 可选的研究主题描述 (如果为空则从文件读取)
    """
    project_dir = f"projects/{project_name}"

    # 检查项目目录是否存在
    if not Path(project_dir).exists():
        print(f"错误: 项目目录不存在: {project_dir}")
        print(f"请先创建项目目录: mkdir -p {project_dir}/{{input,idea,exp,paper}}")
        return

    # 读取研究方向文件
    directions_file = Path(project_dir) / "input" / "research_directions.md"
    if not directions_file.exists():
        print(f"错误: 研究方向文件不存在: {directions_file}")
        return

    research_directions = directions_file.read_text(encoding="utf-8")

    # 如果提供了命令行研究主题，则覆盖文件内容
    if research_topic:
        research_directions = f"# 研究方向\n\n{research_topic}"

    # 创建应用
    app = create_research_app()

    # 初始状态
    initial_state = {
        "project_dir": project_dir,
        "research_directions": research_directions,
        "current_stage": "ideation",
        "completed_agents": [],
        "messages": [],
        "error": "",
    }

    # 执行工作流
    print(f"🚀 启动 LightFARS 研究工作流...")
    print(f"📁 项目目录: {project_dir}")
    print(f"📄 研究主题: {project_name}")
    print("-" * 50)

    # 配置（Checkpointer 需要 thread_id）
    config = {"configurable": {"thread_id": f"research-thread-{project_name}"}}

    result = app.invoke(initial_state, config=config)

    # 输出结果
    print("\n" + "=" * 50)
    print(f"✅ 工作流完成！")
    print(f"最终阶段: {result['current_stage']}")
    print(f"已完成的 Agent: {', '.join(result['completed_agents'])}")
    print("\n输出文件:")
    print(f"  📄 提案: {project_dir}/idea/proposal.md")
    print(f"  📊 计划: {project_dir}/idea/plan.json")
    print(f"  🔬 实验: {project_dir}/exp/")
    print(f"  📝 论文: {project_dir}/paper/final/")
    print("=" * 50)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="LightFARS - 全自动研究系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

  # 运行已有项目
  python run_research.py my-research

  # 运行示例项目
  python run_research.py prompt-engineering-research

  # 创建新项目
  mkdir -p projects/new-research/{input,idea,exp,paper}
  echo "# 研究主题" > projects/new-research/input/research_directions.md
  python run_research.py new-research
        """
    )

    parser.add_argument(
        "project",
        help="项目名称 (对应 projects/ 下的目录名)"
    )

    parser.add_argument(
        "-t", "--topic",
        help="研究主题描述 (可选，覆盖文件内容)"
    )

    args = parser.parse_args()

    run_research(args.project, args.topic)


if __name__ == "__main__":
    main()
