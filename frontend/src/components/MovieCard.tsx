import { Movie } from '../types';

interface MovieCardProps {
  movie: Movie;
}

// 根据电影类型生成颜色
function getGenreColor(genre: string): string {
  const colors: Record<string, string> = {
    '喜剧': 'bg-yellow-500',
    '动作': 'bg-red-500',
    '爱情': 'bg-pink-500',
    '科幻': 'bg-blue-500',
    '恐怖': 'bg-purple-900',
    '剧情': 'bg-green-500',
    '悬疑': 'bg-indigo-500',
    '动画': 'bg-orange-400',
    '犯罪': 'bg-gray-600',
    '冒险': 'bg-teal-500',
  };
  return colors[genre] || 'bg-slate-500';
}

// 生成电影海报占位符
function getPosterPlaceholder(title: string): string {
  const colors = ['from-purple-500 to-pink-500', 'from-blue-500 to-teal-500', 'from-orange-500 to-red-500', 'from-green-500 to-blue-500'];
  const index = title.length % colors.length;
  return colors[index];
}

export default function MovieCard({ movie }: MovieCardProps) {
  return (
    <div className="card-flip w-72 h-96 cursor-pointer">
      <div className="card-flip-inner relative w-full h-full">
        {/* 正面 - 电影信息 */}
        <div className="card-front absolute w-full h-full rounded-2xl overflow-hidden shadow-2xl bg-slate-800 border border-slate-700">
          {/* 海报区域 */}
          <div className={`h-48 bg-gradient-to-br ${getPosterPlaceholder(movie.title)} flex items-center justify-center`}>
            <span className="text-6xl">🎬</span>
          </div>
          
          {/* 信息区域 */}
          <div className="p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-bold text-white truncate flex-1">{movie.title}</h3>
              <span className="text-yellow-400 font-bold ml-2">⭐ {movie.rating}</span>
            </div>
            
            {movie.title_en && (
              <p className="text-slate-400 text-sm mb-2 truncate">{movie.title_en}</p>
            )}
            
            <p className="text-slate-300 text-sm mb-3">{movie.year}年</p>
            
            {/* 类型标签 */}
            <div className="flex flex-wrap gap-1 mb-3">
              {movie.genres.slice(0, 3).map((genre) => (
                <span
                  key={genre}
                  className={`${getGenreColor(genre)} text-white text-xs px-2 py-1 rounded-full`}
                >
                  {genre}
                </span>
              ))}
            </div>
            
            <p className="text-slate-400 text-sm line-clamp-2">{movie.description}</p>
          </div>
        </div>

        {/* 背面 - 推荐理由 */}
        <div className="card-back absolute w-full h-full rounded-2xl overflow-hidden shadow-2xl bg-gradient-to-br from-indigo-600 to-purple-700 border border-indigo-500 p-6 flex flex-col justify-center">
          <h4 className="text-white text-xl font-bold mb-4 text-center">💡 推荐理由</h4>
          <p className="text-white text-base leading-relaxed">{movie.reason}</p>
          <div className="mt-4 text-center">
            <span className="text-indigo-200 text-sm">悬停查看电影详情</span>
          </div>
        </div>
      </div>
    </div>
  );
}
