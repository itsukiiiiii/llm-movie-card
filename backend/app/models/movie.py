"""
电影推荐数据模型
Movie Recommendation Data Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MovieCard(BaseModel):
    """电影推荐卡片数据模型"""
    
    title: str = Field(..., description="电影名称")
    year: str = Field(..., description="上映年份")
    director: str = Field(default="未知导演", description="导演名称")
    reason_for_recommendation: str = Field(
        ..., 
        description="个性化推荐理由（最多2句话）",
        max_length=500
    )
    mood_tags: List[str] = Field(
        default_factory=list,
        description="心情/风格标签列表"
    )
    color_hex: str = Field(
        default="#1E293B", 
        description="代表电影氛围的十六进制颜色代码"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "银翼杀手",
                "year": "1982",
                "director": "雷德利·斯科特",
                "reason_for_recommendation": "这部经典科幻电影完美诠释了人工智能与人类意识的边界，视觉风格独树一帜，非常适合喜欢深度思考的你。",
                "mood_tags": ["科幻", "人工智能", "黑色电影", "经典"],
                "color_hex": "#0F172A"
            }
        }


class RecommendRequest(BaseModel):
    """推荐请求模型"""
    
    user_input: str = Field(
        ..., 
        description="用户输入的心情、场景或偏好描述",
        min_length=2,
        max_length=500
    )
    num_recommendations: int = Field(
        default=1,
        ge=1,
        le=5,
        description="推荐电影数量"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_input": "我想看一部关于人工智能的科幻电影",
                "num_recommendations": 1
            }
        }


class RecommendResponse(BaseModel):
    """推荐响应模型"""
    
    success: bool = Field(..., description="请求是否成功")
    data: dict = Field(..., description="推荐数据")
    error: Optional[str] = Field(default=None, description="错误信息")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "cards": [
                        {
                            "title": "银翼杀手",
                            "year": "1982",
                            "director": "雷德利·斯科特",
                            "reason_for_recommendation": "这部经典科幻电影完美诠释了人工智能与人类意识的边界，视觉风格独树一帜，非常适合喜欢深度思考的你。",
                            "mood_tags": ["科幻", "人工智能", "黑色电影", "经典"],
                            "color_hex": "#0F172A"
                        }
                    ]
                },
                "error": None,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    
    status: str
    service: str
    version: str = "1.0.0"
    llm_provider: str = "SiliconFlow"
