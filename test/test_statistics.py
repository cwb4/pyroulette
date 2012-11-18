import math
import statistics

def test_stats():
    sample = [9, 8, 5, 9, 9, 5, 4, 8, 10, 7, 8, 8]
    actual = statistics.mean(sample)
    expected = 7.5
    assert abs(actual - expected) < 0.001
    actual = statistics.stdev(sample)
    expected = 1.88293
    assert abs(actual - expected) < 0.001
