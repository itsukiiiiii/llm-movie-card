export interface Movie {
  title: string;
  title_en?: string;
  year: number;
  rating: number;
  genres: string[];
  description: string;
  poster_url?: string;
  reason: string;
}

export interface RecommendResponse {
  success: boolean;
  movies: Movie[];
  query: string;
}

export interface HistoryItem {
  id: number;
  query: string;
  movies: Movie[];
  created_at: string;
}
