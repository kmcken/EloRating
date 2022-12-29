import numpy as np


def logistic_score(score_difference, k=10, x0=0):
    """
    Converts match placement to a logistic distribution score
    :param score_difference: match score percentage
    :type score_difference: float
    :param k: logistic growth rate
    :type k: float
    :param x0: curve center
    :type x0: float
    :return: logistic score between 0 and 1
    :rtype: float
    """
    return 1 / (1 + np.exp(-k * (score_difference / 100 - x0)))


def expected_score(Ra, Rb, scale=400):
    """
    Calculates the expected score of Competitor A against Competitor B
    :param Ra: Rating of Competitor A
    :type Ra: int
    :param Rb: Rating of Competitor B
    :type Rb: int
    :param scale: equation constant
    :type scale: float
    :return: Expected Score for Competitor A
    :rtype: float
    """
    return 1 / (1 + 10 ** ((Rb - Ra) / scale))


def expected_ratio(Ra, Rb, scale=400):
    """
    Calculates the expected score ratio of Competitor A against Competitor B
    :param Ra: Rating of Competitor A
    :type Ra: int
    :param Rb: Rating of Competitor B
    :type Rb: int
    :param scale: equation constant
    :type scale: float
    :return: Expected Score for Competitor A
    :rtype: float
    """
    return 10 ** (Ra / scale) / 10 ** (Rb / scale)


def k_factor(number_matches, floor=20):
    """
    K factor depends on number of matches completed.
    :param number_matches: number of previous matches
    :type number_matches: int
    :param floor: maximum ratings change after 5 matches
    :type floor: float
    :return: K factor
    :rtype: float
    """

    k = 100 / (number_matches + 1)
    if k <= floor:
        return floor
    return k


def rating_adjustment(ratings, scores, k):
    """
    Calculates the ratings adjustment for all competitors
    :param ratings: array of competitor ratings
    :type ratings: np.array
    :param scores: array of match scores (percentage)
    :type scores: np.array
    :param k: array of k-factor per competitor
    :type k: np.array
    :return: ratings adjustment
    :rtype: np.array
    """

    N = len(ratings)
    adj = np.zeros(N)
    for i in range(0, N):
        S, E = 0, 0
        for j in range(0, N):
            if i == j:
                pass
            else:
                S += logistic_score(scores[i] - scores[j])
                E += expected_score(ratings[i], ratings[j])
        adj[i] = k[i] * (S - E)

    return adj


def performance_rating(ratings, scores, scale=400):
    """
    Calculates the performance score for the match.

    :param ratings: array of competitor ratings
    :type ratings: np.array
    :param scores: array of match scores (percentage)
    :type scores: np.array
    :param scale: equation constant
    :type scale: float
    :return: performance rating
    :rtype: float
    """

    N = len(ratings)
    perf = np.zeros(N)
    for i in range(0, N):
        S = 0
        for j in range(0, N):
            S += logistic_score(scores[i] - scores[j])
        print(S)
        perf[i] = (np.sum(ratings) + scale * S) / N
    return perf
