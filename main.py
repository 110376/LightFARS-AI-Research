"""主入口"""

import sys
import io
from pathlib import Path
from src.workflows.research_flow import create_research_app

# Fix Windows terminal encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    """主函数"""
    # 创建应用
    app = create_research_app()

    # 初始状态
    # ============ 修改这里：设置你的项目目录 ============
    project_name = "my-research"  # 改成你的项目名称

    initial_state = {
        "project_dir": f"projects/{project_name}",
        # 研究方向将从 input/research_directions.md 自动读取
        "research_directions": Path(f"projects/{project_name}/input/research_directions.md").read_text(encoding="utf-8"),
        "current_stage": "ideation",
        "completed_agents": [],
        "messages": [],
        "error": "",
    }

    # 执行工作流
    print("🚀 启动 LightFARS 研究工作流...")

    # 配置（Checkpointer 需要 thread_id）
    config = {"configurable": {"thread_id": f"research-thread-{project_name}"}}

    result = app.invoke(initial_state, config=config)

    # 输出结果
    print("\n" + "=" * 50)
    print(f"✅ 工作流完成！")
    print(f"最终阶段：{result['current_stage']}")
    print(f"已完成的 Agent：{result['completed_agents']}")
    print("\n消息：")
    for msg in result["messages"]:
        print(f"  {msg}")
    print("=" * 50)


if __name__ == "__main__":
    main()
