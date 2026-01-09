import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SILICONFLOW_API_KEY: str = os.getenv("SILICONFLOW_API_KEY", "")
    SILICONFLOW_BASE_URL: str = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    SILICONFLOW_MODEL: str = os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen2.5-7B-Instruct")

settings = Settings()
