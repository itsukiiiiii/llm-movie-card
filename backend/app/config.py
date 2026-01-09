"""
配置文件 - 管理应用配置和環境變量
Configuration Management
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """应用设置类"""
    
    # 应用配置
    app_name: str = "智能电影推荐卡片"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 硅基流动 API 配置
    siliconflow_api_key: str
    siliconflow_model: str = "deepseek-ai/DeepSeek-V3"
    siliconflow_api_base: str = "https://api.siliconflow.com/v1"
    siliconflow_max_tokens: int = 1024
    siliconflow_temperature: float = 0.7
    
    # 数据库配置 (可选)
    database_url: Optional[str] = None
    postgres_server: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings()
