"""LightFARS 简易启动器 - 一键开始研究"""

import sys
import io
from pathlib import Path
from src.workflows.research_flow import create_research_app

# Fix Windows terminal encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def create_project(project_name: str, topic: str) -> str:
    """创建项目目录和文件"""
    project_dir = Path(f"projects/{project_name}")

    # 创建目录结构
    (project_dir / "input").mkdir(parents=True, exist_ok=True)
    (project_dir / "idea" / "references").mkdir(parents=True, exist_ok=True)
    (project_dir / "exp" / "results").mkdir(parents=True, exist_ok=True)
    (project_dir / "exp" / "figures").mkdir(parents=True, exist_ok=True)
    (project_dir / "exp" / "data").mkdir(parents=True, exist_ok=True)
    (project_dir / "paper" / "final").mkdir(parents=True, exist_ok=True)

    # 写入研究方向
    directions_file = project_dir / "input" / "research_directions.md"
    directions_file.write_text(f"""# 研究方向：{topic}

## 研究背景
{topic}

## 研究问题
1. 核心问题是什么？
2. 如何验证假设？
3. 预期得到什么结果？

## 初步假设
基于当前文献的初步假设

## 预期成果
研究成果的潜在价值
""", encoding="utf-8")

    return str(project_dir)


def run_research(project_name: str, topic: str):
    """运行研究"""
    # 创建项目
    project_dir = create_project(project_name, topic)

    # 读取研究方向
    research_directions = Path(project_dir, "input", "research_directions.md").read_text(encoding="utf-8")

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
    print(f"\n{'='*60}")
    print(f"   LightFARS - 全自动研究系统")
    print(f"{'='*60}")
    print(f"\n研究主题: {topic}")
    print(f"项目目录: {project_dir}")
    print(f"\n{'='*60}\n")

    config = {"configurable": {"thread_id": f"research-{project_name}"}}
    result = app.invoke(initial_state, config=config)

    # 输出结果
    print(f"\n{'='*60}")
    print(f"   研究完成！")
    print(f"{'='*60}")
    print(f"\n输出文件:")
    print(f"  研究提案: {project_dir}/idea/proposal.md")
    print(f"  研究计划: {project_dir}/idea/plan.json")
    print(f"  实验设计: {project_dir}/exp/")
    print(f"  最终论文: {project_dir}/paper/final/report.md")
    print(f"\n{'='*60}\n")

    return result


def interactive_mode():
    """交互式模式"""
    print("\n" + "="*50)
    print("   LightFARS - 一键启动研究")
    print("="*50 + "\n")

    project_name = input("请输入项目名称 (直接回车使用默认: my-research): ").strip()
    if not project_name:
        project_name = "my-research"

    topic = input("\n请输入研究主题 (例如: AI在教育领域的应用): ").strip()
    if not topic:
        topic = "AI 辅助科学研究"

    print(f"\n开始研究: {topic} ...")
    run_research(project_name, topic)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="LightFARS 简易启动器")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互式模式")
    parser.add_argument("-p", "--project", default="my-research", help="项目名称")
    parser.add_argument("-t", "--topic", help="研究主题")

    args = parser.parse_args()

    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
    else:
        if not args.topic:
            print("错误: 请使用 -t 指定研究主题，或使用 -i 进入交互模式")
            return
        run_research(args.project, args.topic)


if __name__ == "__main__":
    main()
