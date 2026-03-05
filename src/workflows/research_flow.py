"""研究工作流（LangGraph 正确实现）"""

from typing import TypedDict, List
from pathlib import Path

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# ============= 状态定义 =============


class ResearchState(TypedDict):
    """研究工作流状态"""

    project_dir: str
    research_directions: str
    current_stage: str  # ideation / planning / experiment / writing / complete / error
    completed_agents: List[str]
    messages: List[str]
    error: str


# ============= 节点函数 =============


def ideation_node(state: ResearchState) -> dict:
    """Ideation 阶段"""
    from src.agents.ideation import run_ideation_agent

    try:
        result = run_ideation_agent(state["project_dir"])

        return {
            "current_stage": "planning",
            "completed_agents": state["completed_agents"] + ["ideation"],
            "messages": state["messages"] + ["✅ Ideation 阶段完成"],
        }
    except Exception as e:
        return {"error": f"Ideation 阶段失败：{str(e)}", "current_stage": "error"}


def planning_node(state: ResearchState) -> dict:
    """Planning 阶段"""
    from src.agents.planning import run_planning_agent

    try:
        result = run_planning_agent(state["project_dir"])

        return {
            "current_stage": "experiment",
            "completed_agents": state["completed_agents"] + ["planning"],
            "messages": state["messages"] + ["✅ Planning 阶段完成"],
        }
    except Exception as e:
        return {"error": f"Planning 阶段失败：{str(e)}", "current_stage": "error"}


def experiment_node(state: ResearchState) -> dict:
    """Experiment 阶段"""
    from src.agents.experiment import run_experiment_agent

    try:
        result = run_experiment_agent(state["project_dir"])

        return {
            "current_stage": "writing",
            "completed_agents": state["completed_agents"] + ["experiment"],
            "messages": state["messages"] + ["✅ Experiment 阶段完成"],
        }
    except Exception as e:
        return {"error": f"Experiment 阶段失败：{str(e)}", "current_stage": "error"}


def writing_node(state: ResearchState) -> dict:
    """Writing 阶段"""
    from src.agents.writing import run_writing_agent

    try:
        result = run_writing_agent(state["project_dir"])

        return {
            "current_stage": "complete",
            "completed_agents": state["completed_agents"] + ["writing"],
            "messages": state["messages"] + ["✅ Writing 阶段完成"],
        }
    except Exception as e:
        return {"error": f"Writing 阶段失败：{str(e)}", "current_stage": "error"}


# ============= 构建工作流 =============


def create_research_workflow() -> StateGraph:
    """构建研究工作流"""
    workflow = StateGraph(ResearchState)

    # 添加节点
    workflow.add_node("ideation", ideation_node)
    workflow.add_node("planning", planning_node)
    workflow.add_node("experiment", experiment_node)
    workflow.add_node("writing", writing_node)

    # 添加边（顺序执行）
    workflow.set_entry_point("ideation")
    workflow.add_edge("ideation", "planning")
    workflow.add_edge("planning", "experiment")
    workflow.add_edge("experiment", "writing")
    workflow.add_edge("writing", END)

    return workflow


def create_research_app():
    """创建研究应用（带持久化）"""
    workflow = create_research_workflow()

    # 添加检查点（用于状态持久化）
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)

    return app
