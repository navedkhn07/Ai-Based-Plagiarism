"""
Lightweight plagiarism detector for low-resource deployments.
Does NOT use heavy ML libraries. Instead uses heuristics based on
duplicate words, sentence repetition, and common phrases.
Suitable for free tiers such as Render 512 MB.
"""
import re
from collections import Counter


class SimplePlagiarismDetector:
    """Heuristic-only detector that mimics the API of the full detector."""

    def __init__(self):
        self.model_name = "simple-heuristic"

    def is_model_loaded(self):
        return True

    def _split_sentences(self, text):
        sentences = re.split(r"[.!?]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _tokenize(self, text):
        return re.findall(r"\w+", text.lower())

    def _ai_heuristic(self, sentences):
        if not sentences:
            return 0.0
        lengths = [len(s) for s in sentences]
        avg = sum(lengths) / len(lengths)
        variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
        uniformity = max(0.0, 1.0 - min(variance / (avg + 1e-6), 1.0))
        repetition = 1.0 - (len(set(sentences)) / len(sentences))
        return (uniformity * 0.5) + (repetition * 0.5)

    def detect_plagiarism(self, text):
        sentences = self._split_sentences(text)
        tokens = self._tokenize(text)
        token_count = len(tokens)
        unique_count = len(set(tokens))

        if token_count == 0:
            similarity_score = 0.0
        else:
            repetition_ratio = 1 - (unique_count / token_count)
            similarity_score = max(0.0, min(100.0, repetition_ratio * 120))

        ai_score = self._ai_heuristic(sentences) * 100

        matches = []
        if similarity_score > 30 and sentences:
            top_sentence = sentences[0][:200]
            matches.append({
                "text": top_sentence,
                "similarity": similarity_score,
                "match_type": "heuristic",
                "source": "Heuristic Analysis",
                "url": "",
                "match_number": 1
            })

        analysis = []
        if similarity_score >= 70:
            analysis.append({
                "type": "High Plagiarism Risk",
                "description": "Heuristic detector flagged significant repetition.",
                "confidence": similarity_score
            })
        elif similarity_score >= 40:
            analysis.append({
                "type": "Moderate Plagiarism Risk",
                "description": "Repeated patterns detected – review recommended.",
                "confidence": similarity_score
            })
        else:
            analysis.append({
                "type": "Low Plagiarism Risk",
                "description": "Text appears mostly unique under heuristic checks.",
                "confidence": 100 - similarity_score
            })

        if ai_score > 55:
            analysis.append({
                "type": "Possible AI-Generated Text",
                "description": "Sentence structure looks uniform or repetitive.",
                "confidence": ai_score
            })

        return {
            "similarity_score": float(similarity_score),
            "plagiarism_percentage": float(similarity_score),
            "exact_match_percentage": 0.0,
            "partial_match_percentage": float(similarity_score),
            "unique_content_percentage": float(100 - similarity_score),
            "matches": matches,
            "analysis": analysis,
            "ai_detection": {
                "is_ai_generated": bool(ai_score > 55),
                "ai_confidence": float(ai_score),
                "repetition_score": float(similarity_score),
                "uniformity_score": float(ai_score)
            },
            "text_length": len(text),
            "sentence_count": len(sentences)
        }

