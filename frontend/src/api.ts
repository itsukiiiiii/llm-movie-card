import axios from 'axios';
import { RecommendResponse, HistoryItem } from './types';

const api = axios.create({
  baseURL: '/api',
});

export async function getRecommendations(prompt: string, count: number = 3): Promise<RecommendResponse> {
  const response = await api.post<RecommendResponse>('/recommend', { prompt, count });
  return response.data;
}

export async function getHistory(): Promise<HistoryItem[]> {
  const response = await api.get<HistoryItem[]>('/history');
  return response.data;
}
