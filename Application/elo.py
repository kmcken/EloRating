import numpy as np


def expected_scores(ratings, scale=1000):
    """
    Expected scores of all competitors

    Parameters
    ----------
    ratings : array like
        Competitors' pre-match ratings
    scale : real number
        Distribution scale factor

    Returns
    -------
    expected : ndarray
        Expect scores as a fraction of all scores
    """

    def expected_score(Ra, Rb, D):
        return 1 / (1 + 10 ** ((Rb - Ra) / D))

    N = len(ratings)
    expected = np.zeros(N)
    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                expected[i] += expected_score(ratings[i], ratings[j], D=scale) / (N * (N - 1) / 2)

    return expected


def expected2(ratings, scale=1000):
    def expected_score(Ra, Rb, D):
        return 2 / (1 + 10 ** ((Rb - Ra) / D))

    N = len(ratings)
    expected = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                expected[i] += expected_score(ratings[i], ratings[j], D=scale) / (N * (N - 1))
    return expected


def scores_normalized(scores, method='floor'):
    """
    Normalizes all scores such that all scores sum to 1

    Parameters
    ----------
    scores : array like
        All competitors scores
    method : str
        floor - Scores are a ratio of the sum / total with the lowest score subtracted first
        percent - Fraction of max score

    Returns
    -------
    normal : ndarray
        Normalized scores as a fraction of all scores
    """

    if method == 'floor':
        N = len(scores)
        normal = np.zeros(N)
        scores = scores - np.min(scores)
        for i in range(0, N):
            normal[i] = scores[i] / np.sum(scores)
        return normal
    if method == 'percent':
        return scores / np.max(scores)


def rating_adjustment(ratings, scores, k=20, scale=1000, min_rating=100):
    """
    Expected scores of all competitors

    Parameters
    ----------
    ratings : array like
        Competitors' pre-match ratings
    scores : array like
        All competitors' scores
    k : array like
        All competitors' k-factor
    scale : real number
        Distribution scale factor
    min_rating : int
        Minimum rating a competitor can have

    Returns
    -------
    ratings_new : ndarray
        Adjusted ratings
    """

    if len(ratings) != len(scores):
        raise ValueError("The length of 'ratings' and 'scores' are not the same.")
    if isinstance(k, int) or isinstance(k, float):
        k = np.ones(len(ratings)) * k

    def adjust(Ra, Ea, Sa, K, N):
        return Ra + K * (N - 1) * (Sa - Ea)

    expected = expected2(ratings, scale=scale)
    scores_norm = scores_normalized(scores, method='floor')

    N = len(ratings)
    ratings_new = np.zeros(N)
    for i in range(0, N):
        ratings_new[i] = adjust(ratings[i], expected[i], scores_norm[i], k[i], N)

    for i in range(N):
        if ratings_new[i] < 100:
            ratings_new[i] = 100
    return np.round(ratings_new, 0)


# def performance_rating(ratings, scores, scale=400):
#     """
#     Calculates the performance score for the match.
#
#     :param ratings: array of competitor ratings
#     :type ratings: np.array
#     :param scores: array of match scores (percentage)
#     :type scores: np.array
#     :param scale: equation constant
#     :type scale: float
#     :return: performance rating
#     :rtype: float
#     """
#
#     N = len(ratings)
#     perf = np.zeros(N)
#     total_score = np.sum(scores)
#     score = score_exponential(scores)
#     for i in range(0, N):
#         S = 0
#         for j in range(0, N):
#             S += (scores[i] - scores[j]) / total_score
#         perf[i] = (np.sum(ratings) + scale * S) / N
#     return perf
