# LLM 电影推荐卡片

一个基于大语言模型的智能电影推荐应用。输入你的观影偏好，AI 为你推荐合适的电影并以精美卡片展示。

## ✨ 功能特点

- 🎬 **智能推荐**：基于硅基流动 Qwen-2.5-7B 模型，理解自然语言描述
- 🃏 **卡片展示**：精美的翻转卡片，正面显示电影信息，背面显示推荐理由
- 📜 **历史记录**：保存推荐历史，随时回顾

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React + TypeScript + Tailwind CSS + Vite |
| 后端 | Python + FastAPI |
| 数据库 | SQLite |
| LLM | 硅基流动 API (Qwen-2.5-7B) |
| 容器化 | Docker + Docker Compose |

## 🚀 快速开始

### 使用 Docker Compose（推荐）

```bash
# 克隆项目
git clone https://github.com/itsukiiiiii/llm-movie-card.git
cd llm-movie-card

# 配置 API Key（重要！）
cp .env.example .env
# 编辑 .env 文件，填入你的硅基流动 API Key

# 启动服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000
```

### 本地开发

#### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 创建 .env 文件并配置 API Key
uvicorn app.main:app --reload --port 8000
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

## 📁 项目结构

```
llm-movie-card/
├── frontend/                # 前端 React 项目
│   ├── src/
│   │   ├── components/      # React 组件
│   │   ├── App.tsx          # 主应用
│   │   ├── api.ts           # API 服务
│   │   └── types.ts         # 类型定义
│   ├── Dockerfile
│   └── package.json
│
├── backend/                 # 后端 FastAPI 项目
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── models.py        # 数据模型
│   │   ├── llm_service.py   # LLM 服务
│   │   ├── database.py      # 数据库操作
│   │   └── config.py        # 配置
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/                    # 文档
│   └── REQUIREMENTS.md      # 需求文档
│
├── docker-compose.yml       # Docker 编排
└── README.md
```

## 🔌 API 接口

### 获取电影推荐

```http
POST /api/recommend
Content-Type: application/json

{
  "prompt": "推荐一部轻松的喜剧电影",
  "count": 3
}
```

### 获取推荐历史

```http
GET /api/history
```

### 健康检查

```http
GET /api/health
```

## 📝 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| SILICONFLOW_API_KEY | 硅基流动 API Key | - |
| SILICONFLOW_BASE_URL | API 地址 | https://api.siliconflow.cn/v1 |
| SILICONFLOW_MODEL | 模型名称 | Qwen/Qwen2.5-7B-Instruct |

## 📄 License

MIT
