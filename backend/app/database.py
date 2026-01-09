import sqlite3
import json
from datetime import datetime
from typing import List
from contextlib import contextmanager
from app.models import Movie, HistoryItem

DATABASE_PATH = "movie_recommendations.db"


def init_db():
    """初始化数据库"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                movies TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


@contextmanager
def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def save_recommendation(query: str, movies: List[Movie]) -> int:
    """保存推荐记录"""
    movies_json = json.dumps([m.model_dump() for m in movies], ensure_ascii=False)
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO recommendations (query, movies) VALUES (?, ?)",
            (query, movies_json)
        )
        conn.commit()
        return cursor.lastrowid


def get_history(limit: int = 20) -> List[HistoryItem]:
    """获取推荐历史"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM recommendations ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        
        history = []
        for row in rows:
            movies = [Movie(**m) for m in json.loads(row["movies"])]
            history.append(HistoryItem(
                id=row["id"],
                query=row["query"],
                movies=movies,
                created_at=datetime.fromisoformat(row["created_at"])
            ))
        return history
