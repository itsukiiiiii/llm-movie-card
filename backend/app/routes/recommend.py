"""
电影推荐API路由
Movie Recommendation API Routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
from app.models.movie import RecommendRequest, RecommendResponse
from app.services.llm_service import llm_service, LLMServiceError

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
async def get_movie_recommendations(request: RecommendRequest):
    """
    获取电影推荐
    
    根据用户输入的心情、场景或偏好，生成个性化的电影推荐卡片。
    
    - **user_input**: 用户描述（必填）
    - **num_recommendations**: 推荐数量（默认1，最大5）
    """
    try:
        # 调用LLM服务获取推荐
        movie_cards = await llm_service.get_recommendations(
            user_input=request.user_input,
            num_recommendations=request.num_recommendations
        )
        
        # 构建响应
        response = RecommendResponse(
            success=True,
            data={
                "cards": [card.model_dump() for card in movie_cards],
                "request_text": request.user_input,
            },
            error=None,
            timestamp=datetime.now()
        )
        
        return response
        
    except LLMServiceError as e:
        logger.error(f"LLM服务错误: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "error": str(e),
                "message": "暂时无法获取推荐，请稍后再试"
            }
        )
    
    except Exception as e:
        logger.error(f"推荐请求处理失败: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "服务器内部错误"
            }
        )


@router.get("/recommend/examples")
async def get_recommendation_examples():
    """获取推荐请求示例"""
    return {
        "examples": [
            {
                "user_input": "我想看一部关于人工智能的科幻电影",
                "num_recommendations": 1
            },
            {
                "user_input": "刚分手想哭一场",
                "num_recommendations": 2
            },
            {
                "user_input": "周末想看轻松的喜剧",
                "num_recommendations": 3
            },
            {
                "user_input": "80年代的经典科幻片",
                "num_recommendations": 1
            },
            {
                "user_input": "喜欢黑客帝国的风格",
                "num_recommendations": 2
            }
        ]
    }


@router.post("/recommend/batch")
async def get_batch_recommendations(requests: list[RecommendRequest]):
    """
    批量获取电影推荐（实验功能）
    
    同时处理多个推荐请求。
    """
    results = []
    
    for i, request in enumerate(requests):
        try:
            movie_cards = await llm_service.get_recommendations(
                user_input=request.user_input,
                num_recommendations=request.num_recommendations
            )
            
            results.append({
                "index": i,
                "success": True,
                "cards": [card.model_dump() for card in movie_cards]
            })
        except Exception as e:
            results.append({
                "index": i,
                "success": False,
                "error": str(e)
            })
    
    return {
        "success": all(r["success"] for r in results),
        "results": results,
        "timestamp": datetime.now()
    }
