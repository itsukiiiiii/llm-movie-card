import { useState } from 'react';
import MovieCard from './components/MovieCard';
import { getRecommendations, getHistory } from './api';
import { Movie, HistoryItem } from './types';

function App() {
  const [prompt, setPrompt] = useState('');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');
    setMovies([]);

    try {
      const response = await getRecommendations(prompt.trim());
      setMovies(response.movies);
    } catch (err) {
      setError('获取推荐失败，请稍后重试');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleShowHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
      setShowHistory(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectHistory = (item: HistoryItem) => {
    setMovies(item.movies);
    setPrompt(item.query);
    setShowHistory(false);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* 标题 */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🎬 LLM 电影推荐卡片
          </h1>
          <p className="text-slate-300 text-lg">
            告诉我你想看什么类型的电影，AI 为你智能推荐
          </p>
        </div>

        {/* 输入区域 */}
        <form onSubmit={handleSubmit} className="mb-12">
          <div className="flex flex-col sm:flex-row gap-4 max-w-2xl mx-auto">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="例如：推荐一部治愈系的日本动画电影..."
              className="flex-1 px-6 py-4 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 transition-colors"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !prompt.trim()}
              className="px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  推荐中...
                </span>
              ) : (
                '获取推荐'
              )}
            </button>
          </div>
          <div className="text-center mt-4">
            <button
              type="button"
              onClick={handleShowHistory}
              className="text-slate-400 hover:text-white transition-colors"
            >
              📜 查看历史记录
            </button>
          </div>
        </form>

        {/* 错误提示 */}
        {error && (
          <div className="text-center mb-8">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* 电影卡片展示 */}
        {movies.length > 0 && (
          <div className="flex flex-wrap justify-center gap-8">
            {movies.map((movie, index) => (
              <MovieCard key={`${movie.title}-${index}`} movie={movie} />
            ))}
          </div>
        )}

        {/* 初始提示 */}
        {!loading && movies.length === 0 && !error && (
          <div className="text-center text-slate-400">
            <p className="text-6xl mb-4">🍿</p>
            <p>输入你的观影需求，开始探索精彩电影吧！</p>
          </div>
        )}

        {/* 历史记录弹窗 */}
        {showHistory && (
          <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
            <div className="bg-slate-800 rounded-2xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-white">📜 推荐历史</h2>
                <button
                  onClick={() => setShowHistory(false)}
                  className="text-slate-400 hover:text-white"
                >
                  ✕
                </button>
              </div>
              {history.length === 0 ? (
                <p className="text-slate-400 text-center py-8">暂无历史记录</p>
              ) : (
                <div className="space-y-3">
                  {history.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => handleSelectHistory(item)}
                      className="w-full text-left p-4 rounded-xl bg-slate-700 hover:bg-slate-600 transition-colors"
                    >
                      <p className="text-white font-medium truncate">{item.query}</p>
                      <p className="text-slate-400 text-sm mt-1">
                        {item.movies.length} 部电影 · {new Date(item.created_at).toLocaleString('zh-CN')}
                      </p>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
