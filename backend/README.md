---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100fd35241738b908287ef41f67366935592fcdfe3b69d3a87e11b4ec35f47348e40221009402267cb071ae8c42c7bf61aa45568ee1845b8935be85f03c1644a983b1f310
    ReservedCode2: 304502210095fd8d613095883712d6ba2bd42a9df7595dc830ef0a0ae9573e9bbc2358640102205a32f8e9da91ced83297781ccdc39d4bffc1f1d23535f560ca8db225b334896e
---

# Smart Movie Card - Backend
# 智能電影推薦卡片後端服務

## 項目簡介
本項目提供智能電影推薦API服務，基於硅基流動LLM生成個性化電影推薦卡片。

## 技術棧
- **Framework**: FastAPI
- **LLM Provider**: SiliconFlow API
- **Database**: PostgreSQL (可選)
- **Container**: Docker

## 快速開始

### 1. 環境配置
```bash
# 複製環境變量模板
cp .env.example .env

# 編輯.env文件，填入你的API Key
SILICONFLOW_API_KEY=your_api_key_here
```

### 2. 本地運行
```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動服務
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Docker部署
```bash
# 構建並啟動容器
docker-compose up --build

# 服務將在以下地址運行
# - API文檔: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

## API接口

### 電影推薦接口
- **Endpoint**: `POST /api/v1/recommend`
- **描述**: 根據用戶輸入生成電影推薦卡片
- **請求體**:
```json
{
  "user_input": "我想看一部關於人工智能的科幻電影",
  "num_recommendations": 1
}
```

### 響應示例
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "title": "銀翼殺手",
        "year": "1982",
        "director": "雷德利·斯科特",
        "reason_for_recommendation": "這部經典科幻電影完美詮釋了人工智能與人類意識的邊界，視覺風格獨樹一幟，非常適合喜歡深度思考的你。",
        "mood_tags": ["科幻", "人工智能", "黑色電影", "經典"],
        "color_hex": "#0F172A"
      }
    ]
  }
}
```

## 項目結構
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI主入口
│   ├── config.py            # 配置管理
│   ├── models/              # 數據模型
│   │   ├── __init__.py
│   │   └── movie.py         # 電影推薦模型
│   ├── services/            # 業務邏輯層
│   │   ├── __init__.py
│   │   └── llm_service.py   # LLM服務集成
│   └── routes/              # API路由
│       ├── __init__.py
│       └── recommend.py     # 推薦相關接口
├── requirements.txt         # Python依賴
├── Dockerfile              # Docker配置
└── .env.example            # 環境變量模板
```

## 環境變量

| 變量名 | 描述 | 必填 |
|--------|------|------|
| SILICONFLOW_API_KEY | 硅基流動API密鑰 | 是 |
| SILICONFLOW_MODEL | 使用的模型名稱（可選） | 否 |
| POSTGRES_SERVER | PostgreSQL服務器地址 | 否 |
| POSTGRES_USER | 用戶名 | 否 |
| POSTGRES_PASSWORD | 密碼 | 否 |
| POSTGRES_DB | 數據庫名稱 | 否 |

## 模型選擇

推薦使用以下硅基流動模型：
- `deepseek-ai/DeepSeek-V3` - 性價比高，智能程度好
- `Qwen/Qwen2.5-72B-Instruct` - 指令遵循能力強
- `THUDM/GLM-4-9B` - 中文表現優秀

## 開發計劃

- [x] 基礎FastAPI框架搭建
- [x] 硅基流動API集成
- [x] 電影推薦Prompt工程
- [ ] 數據庫集成（可選）
- [ ] 前端React應用
- [ ] Docker優化
- [ ] 完整測試覆蓋

## License

MIT License
