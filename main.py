"""主入口"""

from pathlib import Path
from src.workflows.research_flow import create_research_app


def main():
    """主函数"""
    # 创建应用
    app = create_research_app()

    # 初始状态
    initial_state = {
        "project_dir": "projects/prompt-engineering-research",
        "research_directions": """
# 研究方向

探索不同 Prompt 策略对 LLM 代码生成质量的影响。

对比：
- Zero-shot prompting（零样本提示）
- Few-shot prompting（少样本提示）
- Chain-of-Thought prompting（思维链提示）

假设：CoT 提示在复杂算法任务上优于 Zero-shot。
""",
        "current_stage": "ideation",
        "completed_agents": [],
        "messages": [],
        "error": "",
    }

    # 执行工作流
    print("🚀 启动 LightFARS 研究工作流...")

    # 配置（Checkpointer 需要 thread_id）
    config = {"configurable": {"thread_id": "research-thread-001"}}

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
