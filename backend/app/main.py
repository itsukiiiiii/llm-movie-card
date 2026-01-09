"""
智能电影推荐卡片 - 后端服务主入口
Smart Movie Card Backend Service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import recommend
from app.config import settings
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="智能电影推荐卡片 API",
    description="基于LLM的智能电影推荐服务 - Smart Movie Recommendation Card API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(recommend.router, prefix="/api/v1", tags=["推荐服务"])

# 健康检查接口
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "smart-movie-card-api"}

@app.get("/", tags=["系统"])
async def root():
    """根路径欢迎信息"""
    return {
        "message": "欢迎使用智能电影推荐卡片 API",
        "docs": "/docs",
        "version": "1.0.0",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
