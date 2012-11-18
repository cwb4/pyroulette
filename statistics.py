import math

def mean(values):
    """" Compute the mean of a list of integer values

    """
    return sum(values) / len(values)

def stdev(values):
    """ Compute the standard deviation of a list
    of integer values

    """
    m = mean(values)
    s = 0
    for x in values:
        d = x - m
        s += d * d
    v = s / (len(values) - 1)
    return math.sqrt(v)
