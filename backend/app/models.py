from transformers import pipeline, AutoModelForSequenceClassification
import torch
from typing import Dict
from .config.base import settings
import logging

logger = logging.getLogger(__name__)



class MLModels:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

        
        self.emotion_pipeline = pipeline(
            "text-classification",
            model="SamLowe/roberta-base-go_emotions",
            return_all_scores=True,  
            device=self.device
        )

        
        self.vectara_model = AutoModelForSequenceClassification.from_pretrained(
            "vectara/hallucination_evaluation_model",
            trust_remote_code=True
        ).to(self.device)

    
    def analyze_emotions(self, text):
        try:
            results = self.emotion_pipeline(text)
            if results and len(results) > 0:
                # Results come as a list of dictionaries with label and score
                emotions = results[0]  # Get first result's emotions
                # Sort by score and get top 3
                top_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)[:3]
                return [
                    {
                        "label": emotion["label"],
                        "score": float(emotion["score"])
                    }
                    for emotion in top_emotions
                ]
            return []
        except Exception as e:
            logger.error(f"Error analyzing emotions: {str(e)}")
            return []


    def analyze_hallucination(self, pairs):
        try:
            # Handle None or empty input
            if pairs is None or len(pairs) == 0:
                return []
            
            # Ensure pairs are in the correct format expected by the model
            formatted_pairs = [(str(claim), str(premise)) for claim, premise in pairs]
            results = self.vectara_model.predict(formatted_pairs)
            
            normalized_scores = [max(0.0, min(1.0, float(score))) for score in results]
            
            return normalized_scores
        except Exception as e:
            logger.error(f"Error analyzing hallucination: {str(e)}")
            return [0.0] * (len(pairs) if pairs is not None else 0)

    def get_emotion_scores(self, text: str) -> Dict[str, float]:
        results = self.emotion_pipeline(text)
        return {item['label']: item['score'] for item in results[0]}
    
    def get_hallucination_score(self, text: str) -> float:
        results = self.vectara_model.predict(text)
        return results[0]['score']