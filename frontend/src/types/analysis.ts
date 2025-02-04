export interface AnalysisResult {
  text: string;
  emotion_scores: Record<string, number>;
  hallucination_score: number;
  timestamp: string;
} 