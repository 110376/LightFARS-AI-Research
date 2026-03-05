"""LightFARS Web 界面 - 浏览器中使用"""

import streamlit as st
from pathlib import Path
from src.workflows.research_flow import create_research_app
import json

st.set_page_config(
    page_title="LightFARS - 全自动研究系统",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 LightFARS - 全自动研究系统")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")

    st.markdown("### API 配置")
    st.info("请确保已在 `config/.env` 中配置 API Key")

    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("""
    1. 输入研究主题
    2. 点击「开始研究」
    3. 等待 AI 生成完整研究报告
    """)

# 主界面
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 研究主题")

    # 预设主题
    preset_topics = {
        "自定义": "",
        "AI 教育应用": "探索人工智能在教育领域的应用，如个性化学习、智能辅导系统等",
        "大模型代码生成": "研究大型语言模型在代码生成任务上的表现和优化方法",
        "数学推理能力": "对比不同 LLM 在数学推理任务上的能力差异",
        "医疗 AI 应用": "AI 在医疗诊断、药物发现等领域的应用研究",
        "气候变化分析": "使用 AI 技术分析气候变化数据和预测模型",
    }

    preset = st.selectbox("选择预设主题或自定义", list(preset_topics.keys()))

    if preset == "自定义":
        topic = st.text_area(
            "描述你想研究的主题",
            placeholder="例如：探索不同 Prompt 策略对 LLM 代码生成质量的影响...",
            height=100
        )
    else:
        topic = preset_topics[preset]
        st.text_area("研究主题", topic, height=100, disabled=True)

    project_name = st.text_input("项目名称", value="my-research")

with col2:
    st.subheader("🚀 开始研究")

    if st.button("🔥 开始研究", type="primary", use_container_width=True):
        if not topic:
            st.error("请输入研究主题！")
        else:
            with st.spinner("正在创建研究项目..."):
                # 创建项目目录
                project_dir = Path(f"projects/{project_name}")
                (project_dir / "input").mkdir(parents=True, exist_ok=True)
                (project_dir / "idea/references").mkdir(parents=True, exist_ok=True)
                (project_dir / "exp/results").mkdir(parents=True, exist_ok=True)
                (project_dir / "exp/figures").mkdir(parents=True, exist_ok=True)
                (project_dir / "paper/final").mkdir(parents=True, exist_ok=True)

                # 写入研究方向
                (project_dir / "input" / "research_directions.md").write_text(
                    f"# 研究方向：{topic}\n\n## 研究背景\n{topic}",
                    encoding="utf-8"
                )

            st.success(f"项目已创建: {project_dir}")

            # 显示进度
            progress_bar = st.progress(0)
            status_text = st.empty()

            stages = ["💡 构思阶段", "📋 规划阶段", "🧪 实验阶段", "✍️ 写作阶段"]

            with st.spinner("AI 正在研究中，请稍候..."):
                try:
                    app = create_research_app()
                    research_directions = (project_dir / "input" / "research_directions.md").read_text(encoding="utf-8")

                    initial_state = {
                        "project_dir": str(project_dir),
                        "research_directions": research_directions,
                        "current_stage": "ideation",
                        "completed_agents": [],
                        "messages": [],
                        "error": "",
                    }

                    config = {"configurable": {"thread_id": f"research-{project_name}"}}

                    # 执行（这里会阻塞，实际应用可能需要异步处理）
                    result = app.invoke(initial_state, config=config)

                    for i, stage in enumerate(stages):
                        progress_bar.progress((i + 1) / len(stages))
                        status_text.text(stage)

                    st.success("🎉 研究完成！")

                except Exception as e:
                    st.error(f"研究过程出错: {str(e)}")

    st.markdown("---")
    st.markdown("### 📊 研究阶段")

    for stage in ["💡 构思", "📋 规划", "🧪 实验", "✍️ 写作"]:
        st.markdown(f"- {stage}")

# 显示已有项目
st.markdown("---")
st.subheader("📁 已有项目")

projects_dir = Path("projects")
if projects_dir.exists():
    projects = [p.name for p in projects_dir.iterdir() if p.is_dir()]

    if projects:
        for p in projects:
            with st.expander(f"📂 {p}"):
                # 检查是否有输出文件
                proj_path = projects_dir / p

                if (proj_path / "idea" / "proposal.md").exists():
                    st.markdown("✅ 已生成研究提案")
                    if st.button(f"查看提案", key=f"proposal_{p}"):
                        content = (proj_path / "idea" / "proposal.md").read_text(encoding="utf-8")
                        st.text(content)

                if (proj_path / "paper" / "final" / "report.md").exists():
                    st.markdown("✅ 已生成最终论文")
                    if st.button(f"查看论文", key=f"paper_{p}"):
                        content = (proj_path / "paper" / "final" / "report.md").read_text(encoding="utf-8")
                        st.markdown(content)
    else:
        st.info("暂无项目，请创建第一个研究项目")
else:
    st.info("projects 目录不存在")
