from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import RecommendRequest, RecommendResponse, HistoryItem
from app.llm_service import get_movie_recommendations
from app.database import init_db, save_recommendation, get_history
from typing import List

app = FastAPI(title="LLM Movie Card API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """应用启动时初始化数据库"""
    init_db()


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "LLM Movie Card API is running"}


@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend_movies(request: RecommendRequest):
    """获取电影推荐"""
    try:
        movies = await get_movie_recommendations(request.prompt, request.count)
        
        # 保存到数据库
        save_recommendation(request.prompt, movies)
        
        return RecommendResponse(
            success=True,
            movies=movies,
            query=request.prompt
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐服务出错: {str(e)}")


@app.get("/api/history", response_model=List[HistoryItem])
async def get_recommendation_history():
    """获取推荐历史"""
    return get_history()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
