"""测试新闻摘要 Agent"""

import sys
import io

# Fix Windows terminal encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.agents.news_summarizer import run_news_summarizer


def main():
    print("\n" + "="*60)
    print("   🔬 新闻摘要 Agent - 测试运行")
    print("="*60 + "\n")

    # 获取用户输入
    topic = input("请输入新闻主题 (直接回车使用默认): ").strip()
    if not topic:
        topic = "人工智能最新进展"

    print(f"\n正在分析主题: {topic}")
    print("请稍候...\n")

    # 运行 Agent
    result = run_news_summarizer(topic)

    # 显示结果
    print("\n" + "="*60)
    print("   ✅ 分析完成！")
    print("="*60)
    print(f"\n最终消息:")
    print(result["final_message"])

    # 显示消息数量
    print(f"\n总共 {len(result['all_messages'])} 条消息")

    # 查找生成的报告文件
    import re
    for msg in result["all_messages"]:
        if "报告已保存到" in msg:
            match = re.search(r'报告已保存到：(.+)', msg)
            if match:
                print(f"\n📄 报告文件: {match.group(1).strip()}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
