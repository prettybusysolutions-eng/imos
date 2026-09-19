def score_memory(source_type: str, verified: bool, recency_weight: float = 1.0, repeated: int = 1, endorsed: bool = False) -> float:
    score = 0.2
    if source_type in {'github', 'decision', 'verification', 'memory'}:
        score += 0.2
    if verified:
        score += 0.25
    score += min(recency_weight, 1.0) * 0.15
    score += min(repeated, 5) * 0.03
    if endorsed:
        score += 0.05
    return min(round(score, 3), 1.0)

