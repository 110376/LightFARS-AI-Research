"""测试 Ideation Agent"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.ideation import run_ideation_agent


def test_ideation():
    """测试 Ideation Agent"""
    project_dir = "projects/prompt-engineering-research"

    print("🧪 测试 Ideation Agent...")
    print(f"项目目录：{project_dir}")

    try:
        result = run_ideation_agent(project_dir)

        print("\n✅ 测试成功！")
        print(f"状态：{result['status']}")
        print(f"\n最终消息：\n{result['final_message']}")

    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_ideation()
