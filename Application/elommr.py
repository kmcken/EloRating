from config import *
# Implementation of Elo-MMR(infinite) rating system from "Elo-MMR: A Rating System for Massive Multiplayer Competitions"
# by Ebtekar, A. and Liu, P.


def pdf(x, mean, scale, method='normal'):
    """
    Standard normal distribution probability density function

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        standard deviation
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution

    Returns
    -------
    pdf : ndarray
        Probability density function
    """

    if method == 'logistic':
        d = np.sqrt(3) / np.pi * scale
        const = 0.25 / d
        sech = 2 * np.exp((x - mean) / (scale * np.sqrt(2))) / (np.exp(2 * (x - mean) / (scale * np.sqrt(2))) + 1)
        return const * sech
    return 1 / (scale * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / scale) ** 2)


def pdf_prime(x, mean, scale, method='normal'):
    """
    First derivative of the standard normal distribution probability density function

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        standard deviation
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution

    Returns
    -------
    pdf : ndarray
        Probability density function
    """
    if method == 'logistic':
        d = np.sqrt(3) / np.pi * scale
        return pdf(x, mean, scale, method=method) * (1 - 2 * cdf(x, mean, scale, method=method)) / d
    return - 1 * (x - mean) * pdf(x, mean, scale, method=method) / scale ** 2


def cdf(x, mean, scale, method='normal'):
    """
    Cumulative distribution function

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        standard deviation
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution

    Returns
    -------
    cdf : ndarray
        Cumulative density function
    """

    if method == 'logistic':
        d = np.sqrt(3) / np.pi * scale
        return 0.5 * (1 + np.tanh((x - mean) / (2 * d)))
    return 0.5 * (1 + sp.special.erf((x - mean) / (scale * np.sqrt(2))))


def logistic(x, mean=0, scale=percent_factor):
    """
    Logistic function with output range [-1, 1]

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        scale factor

    Returns
    -------
    cdf : ndarray
        Cumulative density function
    """
    return 1 / (1 + np.exp(-scale * (x - mean)))


def cdf_normal_inverse(percentile, mean, std):
    """
    Standard normal distribution cumulative distribution function

    Parameters
    ----------
    percentile : array like
        percentile
    mean : float
        mean
    std : float
        standard deviation

    Returns
    -------
    x : ndarray
        x value corresponding with the percentile
    """

    return sp.stats.norm.ppf(percentile, loc=mean, scale=std)


def loss_distribution(x, mean, scale, method='normal'):
    """
    Loss distribution

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        standard deviation
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution

    Returns
    -------
    loss : ndarray
        Probability density function
    """
    def linear_region(val, mu=mean, k=scale):
        y1 = pdf(mu + 2 * scale - 10, mu, k, method=method) / (- cdf(-(mu + 2 * k - 10), -mu, k, method=method))
        y2 = pdf(mu + 2 * scale, mu, k, method=method) / (- cdf(-(mu + 2 * k), -mu, k, method=method))
        m = (y2 - y1) / 10
        return m * (val - (mu + 2 * scale)) + y2

    def curved_region(val, mu=mean, k=scale):
        return pdf(val, mu, k, method=method) / (- cdf(-val, -mean, k, method=method))

    return np.piecewise(x, [x <= mean + 2 * scale, x > mean + 2 * scale], [curved_region, linear_region])


def draw_distribution(x, mean, scale, method='logistic'):
    """
    Draw distribution

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        standard deviation
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution

    Returns
    -------
    draw : ndarray
        Probability density function
    """

    return np.divide(pdf_prime(x, mean, scale, method=method), pdf(x, mean, scale, method=method))


def win_distribution(x, mean, scale, method='normal'):
    """
    Win distribution

    Parameters
    ----------
    x : array like
        x value
    mean : float
        mean
    scale : float
        standard deviation
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution

    Returns
    -------
    win : ndarray
        Probability density function
    """
    def linear_region(val, mu=mean, k=scale):
        y1 = pdf(mu - 2 * scale + 10, mu, k, method=method) / (cdf(mu - 2 * k + 10, mu, k, method=method))
        y2 = pdf(mu - 2 * scale, mu, k, method=method) / (cdf(mu - 2 * k, mu, k, method=method))
        m = (y2 - y1) / 10
        return m * (val - (mu - 2 * scale)) + y2

    def curved_region(val, mu=mean, k=scale):
        return pdf(val, mu, k, method=method) / (cdf(val, mean, k, method=method))

    return np.piecewise(x, [x < mean - 2 * scale, x >= mean - 2 * scale], [linear_region, curved_region])


def weight(match_count, placement=noob_placement, min_weight=noob_weight):
    """
    Weights the effect of the competitor relative to how new they are.

    Parameters
    ----------
    match_count : int
        number of matches a competitor has competed in
    placement : int
        max number of placement matches
    min_weight : float
        minimum weight

    Returns
    -------
    weight : float
        new shooter weight
    """

    def linear(x, x_max, y_min):
        if x >= x_max:
            return 1
        if x <= 0:
            return y_min
        return x * (1 - y_min) / x_max + y_min

    w = linear(match_count, placement, min_weight)
    return w

