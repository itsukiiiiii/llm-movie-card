import httpx
import json
from typing import List
from app.config import settings
from app.models import Movie


SYSTEM_PROMPT = """你是一个专业的电影推荐助手。根据用户的描述，推荐合适的电影。

要求：
1. 推荐指定数量的电影
2. 每部电影包含：中文名(title)、英文名(title_en)、年份(year)、评分1-10(rating)、类型数组(genres)、简介(description)、推荐理由(reason)
3. 必须严格按照 JSON 格式返回，不要有任何其他文字

返回格式示例：
{
  "movies": [
    {
      "title": "肖申克的救赎",
      "title_en": "The Shawshank Redemption",
      "year": 1994,
      "rating": 9.7,
      "genres": ["剧情", "犯罪"],
      "description": "一场冤狱，一段传奇，讲述希望与自由的故事",
      "reason": "这是一部关于希望的电影，非常适合需要力量的观众"
    }
  ]
}"""


async def get_movie_recommendations(prompt: str, count: int = 3) -> List[Movie]:
    """调用硅基流动 API 获取电影推荐"""
    
    user_message = f"请推荐 {count} 部电影。用户需求：{prompt}"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.SILICONFLOW_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.SILICONFLOW_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.SILICONFLOW_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
        # 解析 LLM 返回的内容
        content = result["choices"][0]["message"]["content"]
        
        # 尝试解析 JSON
        try:
            # 处理可能的 markdown 代码块
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            data = json.loads(content.strip())
            movies = [Movie(**movie) for movie in data["movies"]]
            return movies
        except (json.JSONDecodeError, KeyError) as e:
            print(f"解析 LLM 响应失败: {e}")
            print(f"原始内容: {content}")
            raise ValueError("无法解析电影推荐结果")
