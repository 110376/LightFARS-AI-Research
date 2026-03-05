"""新闻摘要 Agent - 自定义示例"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import requests
import json
from datetime import datetime

from src.utils.llm import get_llm


# ============= 工具定义 =============

class SearchNewsInput(object):
    """新闻搜索输入"""
    query: str
    max_results: int = 5


@tool
def search_news(query: str, max_results: int = 5) -> str:
    """搜索最新新闻（模拟实现）

    Args:
        query: 搜索关键词
        max_results: 最大结果数

    Returns:
        新闻列表 JSON 字符串
    """
    # 模拟新闻数据（实际可接入真实新闻 API）
    mock_news = [
        {
            "title": f"{query}相关新闻 {i+1}",
            "summary": f"关于{query}的最新报道，包含专家分析和市场趋势...",
            "source": "科技日报",
            "published": datetime.now().strftime("%Y-%m-%d"),
            "url": f"https://example.com/news/{i+1}"
        }
        for i in range(min(max_results, 5))
    ]

    return json.dumps(mock_news, ensure_ascii=False, indent=2)


@tool
def analyze_sentiment(text: str) -> str:
    """分析文本情感倾向

    Args:
        text: 待分析文本

    Returns:
        情感分析结果（正面/负面/中性）
    """
    # 简单实现（实际可用 LLM 或专业 API）
    positive_words = ["增长", "突破", "成功", "上涨", "创新"]
    negative_words = ["下降", "失败", "风险", "下跌", "问题"]

    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)

    if pos_count > neg_count:
        sentiment = "正面"
        confidence = min(0.9, 0.5 + pos_count * 0.1)
    elif neg_count > pos_count:
        sentiment = "负面"
        confidence = min(0.9, 0.5 + neg_count * 0.1)
    else:
        sentiment = "中性"
        confidence = 0.5

    return json.dumps({
        "sentiment": sentiment,
        "confidence": f"{confidence*100:.1f}%",
        "positive_count": pos_count,
        "negative_count": neg_count
    }, ensure_ascii=False, indent=2)


@tool
def write_summary_report(topic: str, content: str) -> str:
    """撰写摘要报告

    Args:
        topic: 主题
        content: 报告内容

    Returns:
        保存路径
    """
    from pathlib import Path

    output_dir = Path("projects/news-reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic}_{timestamp}.md"
    filepath = output_dir / filename

    report = f"""# {topic} - 新闻摘要报告

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{content}

---

*本报告由 LightFARS 新闻摘要 Agent 自动生成*
"""

    filepath.write_text(report, encoding="utf-8")
    return f"✅ 报告已保存到：{filepath}"


# ============= Agent 创建 =============

NEWS_SUMMARIZER_SYSTEM_PROMPT = """你是一位专业的新闻分析师，擅长从海量信息中提取关键内容。

你的能力：
- 搜索最新新闻
- 分析新闻情感倾向
- 撰写简洁的摘要报告

你的工作流程：
1. 根据用户提供的主题搜索相关新闻
2. 分析每条新闻的情感倾向
3. 提取关键信息和要点
4. 生成结构化的摘要报告
5. 保存报告到文件

报告要求：
- 简洁明了（不超过500字）
- 包含3-5条核心新闻
- 标注情感倾向
- 突出重要数据和观点"""


def create_news_summarizer_agent():
    """创建新闻摘要 Agent"""
    llm = get_llm()

    # 工具列表
    tools = [search_news, analyze_sentiment, write_summary_report]

    # 绑定系统提示
    llm_with_system = llm.bind(system=NEWS_SUMMARIZER_SYSTEM_PROMPT)

    # 创建 ReAct Agent
    agent = create_react_agent(llm_with_system, tools)

    return agent


def run_news_summarizer(topic: str) -> dict:
    """运行新闻摘要 Agent

    Args:
        topic: 新闻主题

    Returns:
        执行结果
    """
    agent = create_news_summarizer_agent()

    input_message = HumanMessage(
        content=f"""请为「{topic}」创建一份新闻摘要报告。

要求：
1. 搜索相关新闻（至少5条）
2. 分析每条新闻的情感倾向
3. 提取关键信息
4. 生成摘要报告并保存
"""
    )

    result = agent.invoke({"messages": [input_message]})

    final_message = result["messages"][-1]

    return {
        "status": "success",
        "final_message": final_message.content,
        "all_messages": [msg.content for msg in result["messages"]],
    }


# ============= 快速测试 =============

if __name__ == "__main__":
    print("🔬 新闻摘要 Agent 测试\n")

    result = run_news_summarizer("人工智能最新进展")

    print("\n" + "="*50)
    print("✅ 分析完成！")
    print("="*50)
