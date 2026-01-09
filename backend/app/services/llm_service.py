"""
硅基流动 LLM 服务集成
SiliconFlow LLM Service Integration
"""

import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings
from app.models.movie import MovieCard

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """LLM服务异常"""
    pass


class SiliconFlowService:
    """硅基流动LLM服务类"""
    
    def __init__(self):
        """初始化硅基流动客户端"""
        self.client = OpenAI(
            api_key=settings.siliconflow_api_key,
            base_url=settings.siliconflow_api_base,
        )
        self.model = settings.siliconflow_model
        self.max_tokens = settings.siliconflow_max_tokens
        self.temperature = settings.siliconflow_temperature
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是一位专业的电影推荐专家。你的任务是根据用户的描述，推荐最合适的电影。

请遵循以下规则：
1. 只推荐符合用户描述的电影
2. 推荐理由要个性化、与用户输入相关
3. 选择的颜色要能代表电影的整体氛围
4. 标签要简洁、相关

输出要求：
- 必须返回严格的JSON格式
- 推荐理由不超过2句话
- 标签数量控制在3-5个""""
    
    def _build_user_prompt(self, user_input: str, num_recommendations: int) -> str:
        """构建用户提示词"""
        return f"""请根据以下描述推荐{num_recommendations}部电影：

用户描述：{user_input}

请为每部电影提供以下信息：
1. 电影名称
2. 上映年份
3. 导演
4. 推荐理由（个性化说明为什么这部电影适合用户）
5. 心情/风格标签（3-5个）
6. 代表电影氛围的颜色（十六进制格式，如#0F172A）

请以JSON数组格式返回结果。"""
    
    def _parse_response(self, content: str) -> List[Dict[str, Any]]:
        """解析LLM响应内容"""
        try:
            # 尝试直接解析JSON
            return json.loads(content)
        except json.JSONDecodeError:
            # 尝试提取JSON代码块
            logger.warning("直接解析JSON失败，尝试提取JSON代码块")
            
            # 尝试 ```json ``` 格式
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            try:
                return json.loads(content.strip())
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}")
                logger.error(f"原始内容: {content}")
                raise LLMServiceError("无法解析LLM返回的JSON格式")
    
    def _validate_movie_data(self, movie_data: Dict[str, Any]) -> MovieCard:
        """验证和规范化电影数据"""
        required_fields = ["title", "year", "reason_for_recommendation"]
        
        for field in required_fields:
            if field not in movie_data:
                raise LLMServiceError(f"缺少必要字段: {field}")
        
        # 设置默认值
        if "director" not in movie_data:
            movie_data["director"] = "未知导演"
        
        if "mood_tags" not in movie_data or not movie_data["mood_tags"]:
            movie_data["mood_tags"] = ["电影"]
        
        if "color_hex" not in movie_data or not movie_data["color_hex"]:
            movie_data["color_hex"] = "#1E293B"
        
        return MovieCard(**movie_data)
    
    async def get_recommendations(
        self, 
        user_input: str, 
        num_recommendations: int = 1
    ) -> List[MovieCard]:
        """
        获取电影推荐
        
        Args:
            user_input: 用户输入的描述
            num_recommendations: 推荐数量
            
        Returns:
            电影推荐卡片列表
        """
        try:
            logger.info(f"正在为用户请求生成推荐: {user_input}")
            
            # 构建请求消息
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": self._build_user_prompt(user_input, num_recommendations)},
            ]
            
            # 调用硅基流动API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False,
            )
            
            # 提取响应内容
            content = response.choices[0].message.content
            logger.info(f"LLM响应: {content[:200]}...")
            
            # 解析JSON响应
            movies_data = self._parse_response(content)
            
            # 确保返回的是列表
            if isinstance(movies_data, dict):
                if "movies" in movies_data:
                    movies_data = movies_data["movies"]
                elif "recommendations" in movies_data:
                    movies_data = movies_data["recommendations"]
                elif "cards" in movies_data:
                    movies_data = movies_data["cards"]
                else:
                    movies_data = [movies_data]
            
            if not isinstance(movies_data, list):
                movies_data = [movies_data]
            
            # 验证和规范化数据
            movie_cards = []
            for movie_data in movies_data[:num_recommendations]:
                try:
                    card = self._validate_movie_data(movie_data)
                    movie_cards.append(card)
                except Exception as e:
                    logger.warning(f"验证电影数据失败: {e}")
                    continue
            
            if not movie_cards:
                raise LLMServiceError("未能生成有效的电影推荐")
            
            logger.info(f"成功生成 {len(movie_cards)} 个推荐")
            return movie_cards
            
        except OpenAIError as e:
            logger.error(f"硅基流动API调用失败: {e}")
            raise LLMServiceError(f"LLM服务暂时不可用: {str(e)}")
        except Exception as e:
            logger.error(f"获取推荐失败: {e}")
            raise LLMServiceError(str(e))


# 全局服务实例
llm_service = SiliconFlowService()
