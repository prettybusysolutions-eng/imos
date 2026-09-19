from imos.services.trust_engine import score_memory

def test_verified_scores_higher():
    assert score_memory('memory', True) > score_memory('memory', False)

