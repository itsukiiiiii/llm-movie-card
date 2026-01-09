# LLM 电影推荐卡片 - 需求文档

## 项目概述

**项目名称**：LLM 电影推荐卡片 (LLM Movie Card)

**项目描述**：一个基于大语言模型的智能电影推荐应用。用户输入自己的观影偏好或心情描述，系统通过 LLM 分析后推荐合适的电影，并以精美卡片形式展示电影信息。

**技术栈**：
- 前端：React + TypeScript + Tailwind CSS
- 后端：Python + FastAPI
- 数据库：SQLite（轻量级，适合MVP）
- LLM：硅基流动 API (Qwen-2.5-7B)
- 容器化：Docker + Docker Compose

---

## 功能需求

### MVP 核心功能

#### 1. 电影推荐（核心）
- 用户输入观影偏好描述（如："我想看一部轻松搞笑的喜剧"、"推荐一部类似《盗梦空间》的烧脑电影"）
- 系统调用 LLM 分析用户需求并推荐 3-5 部电影
- 返回电影的基本信息（名称、年份、类型、简介、评分、推荐理由）

#### 2. 电影卡片展示
- 以卡片形式展示推荐的电影
- 卡片包含：电影海报、名称、年份、评分、类型标签、简短描述
- 支持卡片翻转查看详细推荐理由

#### 3. 推荐历史
- 保存用户的推荐历史记录
- 可查看历史推荐结果

---

## 技术架构

### 系统架构图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│    Frontend     │────▶│    Backend      │────▶│  硅基流动 API   │
│    (React)      │     │    (FastAPI)    │     │  (Qwen-2.5-7B)  │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │                 │
                        │     SQLite      │
                        │    Database     │
                        │                 │
                        └─────────────────┘
```

### 目录结构

```
llm-movie-card/
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── components/      # React 组件
│   │   ├── pages/           # 页面
│   │   ├── services/        # API 服务
│   │   ├── types/           # TypeScript 类型
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
│
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/             # API 路由
│   │   ├── core/            # 核心配置
│   │   ├── models/          # 数据模型
│   │   ├── services/        # 业务逻辑
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml       # Docker 编排
├── README.md                # 项目说明
└── docs/                    # 文档
    └── REQUIREMENTS.md
```

---

## API 设计

### 后端 API

#### 1. 获取电影推荐
```
POST /api/recommend
```

**请求体**：
```json
{
  "prompt": "我想看一部轻松的喜剧电影",
  "count": 3
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "movies": [
      {
        "id": 1,
        "title": "怦然心动",
        "title_en": "Flipped",
        "year": 2010,
        "rating": 9.1,
        "genres": ["喜剧", "爱情"],
        "description": "一部关于青春期初恋的温馨喜剧...",
        "poster_url": "https://...",
        "reason": "这部电影节奏轻快，充满幽默感..."
      }
    ],
    "query": "我想看一部轻松的喜剧电影"
  }
}
```

#### 2. 获取推荐历史
```
GET /api/history
```

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "query": "我想看一部轻松的喜剧电影",
      "movies": [...],
      "created_at": "2026-01-09T10:00:00Z"
    }
  ]
}
```

#### 3. 健康检查
```
GET /api/health
```

---

## 数据库设计

### 表结构

#### recommendations 表（推荐记录）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| query | TEXT | 用户输入的查询 |
| result | TEXT | LLM 返回的推荐结果(JSON) |
| created_at | DATETIME | 创建时间 |

---

## LLM Prompt 设计

### 系统提示词
```
你是一个专业的电影推荐助手。根据用户的描述，推荐合适的电影。

要求：
1. 推荐 {count} 部电影
2. 每部电影包含：中文名、英文名、年份、评分(1-10)、类型、简介、推荐理由
3. 以 JSON 格式返回

返回格式：
{
  "movies": [
    {
      "title": "电影中文名",
      "title_en": "English Title",
      "year": 2020,
      "rating": 8.5,
      "genres": ["类型1", "类型2"],
      "description": "电影简介...",
      "reason": "推荐理由..."
    }
  ]
}
```

---

## 开发计划

### 第一阶段：环境搭建（1小时）
- [ ] 初始化 Git 仓库并关联远程
- [ ] 创建项目目录结构
- [ ] 配置 Docker 和 Docker Compose

### 第二阶段：后端开发（2-3小时）
- [ ] 搭建 FastAPI 项目框架
- [ ] 实现硅基流动 API 调用
- [ ] 实现电影推荐接口
- [ ] 实现数据库存储

### 第三阶段：前端开发（2-3小时）
- [ ] 搭建 React 项目
- [ ] 实现输入界面
- [ ] 实现电影卡片组件
- [ ] 实现推荐历史页面

### 第四阶段：集成测试（1小时）
- [ ] 前后端联调
- [ ] Docker 容器化测试
- [ ] 编写 README 文档

---

## 配置信息

### 硅基流动 API
- **API Endpoint**: `https://api.siliconflow.cn/v1/chat/completions`
- **Model**: `Qwen/Qwen2.5-7B-Instruct`
- **API Key**: `sk-sjwrrmlsaqkpkbatycovvegaxofgtsckckrxtsmmtksyxtot`

### Docker 端口配置
- 前端: 3000
- 后端: 8000

---

## 验收标准

1. ✅ 用户可以输入观影偏好描述
2. ✅ 系统能正确调用 LLM 返回推荐结果
3. ✅ 电影以卡片形式美观展示
4. ✅ 推荐历史可以查看
5. ✅ 项目可通过 Docker Compose 一键启动
6. ✅ README 文档完整清晰

---

## 附录

### 参考资源
- [硅基流动 API 文档](https://docs.siliconflow.cn/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [React 文档](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
