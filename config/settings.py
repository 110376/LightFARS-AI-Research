"""配置加载模块（使用 pydantic-settings）"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM 主配置
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model_id: str = "gpt-4o"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4000

    # 备用 LLM
    llm_backup_provider: Optional[str] = None
    llm_backup_api_key: Optional[str] = None
    llm_backup_base_url: Optional[str] = None
    llm_backup_model_id: Optional[str] = None

    # 搜索 API
    serper_api_key: Optional[str] = None
    serper_enabled: bool = False
    arxiv_api_enabled: bool = True
    arxiv_max_results: int = 20

    # 工具配置
    code_executor_timeout: int = 300
    code_executor_sandbox: bool = True
    figure_dpi: int = 300
    figure_format: str = "png"

    # 项目配置
    project_name: str = "lightfars"
    max_iterations: int = 3
    log_level: str = "INFO"
    log_file: str = "logs/lightfars.log"

    # Git 配置
    git_auto_commit: bool = True
    git_commit_message_prefix: str = "[LightFARS]"

    # 状态管理
    state_check_interval: int = 5

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# 全局配置实例
settings = Settings()
