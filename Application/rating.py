from config import *
from Utilities import practiscore as ps
from Application import database, elommr as mmr
import matplotlib.pyplot as plt


class Competitor:
    """
    Competitor info

    Attributes
    ----------
    first : str
        Competitor's First Name
    last : str
        Competitor's Last Name
    member : str
        Competitor's USPSA Number
    division : str
        Competitor's division
    rating : int
        Current rating
    member : float
        Current uncertainty
    performance : int
        Performance rating at last match
    member : int
        Number of matches competed in
    match_id : int
        Practiscore match id number of last match
    match_name : str
        Match name in Practiscore
    club : str
        Club of last match
    club_id : str
        USPSA club ID of last match
    match_type : str
        Type of match of last match
    match_date : str
        Date of last match MMDDYY
    match_date_unit : int
        Date of late match in unix format
    """
    def __init__(self):
        self.first = None
        self.last = None
        self.member = None
        self.division = None
        self.rating = None
        self.noob = None
        self.uncertainty = None
        self.performance = None
        self.last_change = None
        self.number_of_matches = None
        self.match_id = None
        self.match_name = None
        self.club = None
        self.club_code = None
        self.match_type = None
        self.match_date = None
        self.match_date_unix = None
        self.place = None
        self.score = None
        self.percent = None
        self.wins = None
        self.losses = None
        self.stage_count = None
        self.competitor_count = None


def match_update(file, division='Carry Optics', match_type='USPSA'):
    """
    Updates ratings with a given match

    Parameters
    ----------
    file : str
        file path to match .json file
    division : str
        division name
    match_type : str
        Match type
    """
    # Get Scores from match
    scores = ps.mmr_format(file, division)
    competitor_count = len(scores)

    # Sort win/loss rankings
    scores = win_loss_ranking(scores)

    noobs = False
    for i in range(len(scores)):
        scores[i] = database.get_competitor_rating(scores[i])
        if scores[i].noob is True:
            noobs = True

    ## Determine Performance Ratings
    scores = performance_rating(scores, method=mmr_method)

    ## If a noob is in the match, assign performance rating to noob and redo the performance ratings
    if noobs is True:
        # for competitor in scores:
            # if competitor.noob is True:
            #     competitor.rating = competitor.performance
        scores = performance_rating(scores, method=mmr_method)

    ## Update Skill Ratings and uncertainties
    u_match = match_uncertainty(scores)  # uncertainty for the match
    for i in range(len(scores)):
        scores[i] = new_rating(scores[i], u_match, scores[i].stage_count, competitor_count)
    # scores = new_uncertainty(scores, u_match)

    ## Write to database
    for competitor in scores:
        if competitor.member is not None:
            competitor.number_of_matches += 1
            database.write_competitor(competitor)
    return scores


def win_loss_ranking(scores):
    """
    Updates competitors' win/loss rankings

    Parameters
    ----------
    scores : list
        list of Competitors at match

    Returns
    ----------
    scores : list
        original list with updated Competitor info
    """

    N = len(scores)

    for i in range(N):
        win, loss = list(), list()
        for j in range(N):
            win.append((scores[j].place, scores[i].percent - scores[j].percent)) if (scores[j].place > scores[i].place) else False
            loss.append((scores[j].place, scores[i].percent - scores[j].percent)) if (scores[j].place < scores[i].place) else False
        scores[i].wins = win
        scores[i].losses = loss
    return scores


def performance_rating(scores, min_rating=rating_min, max_rating=rating_max, method='normal', plot=False):
    """
    Calculates the performance ratings for all competitors

    Parameters
    ----------
    scores : list
        list of Competitors at match
    min_rating : int
        minimum rating
    max_rating : int
        maximum rating
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution
    plot : bool
        Plot Q

    Returns
    ----------
    scores : list
        original list with updated Competitor info
    """

    M = max_rating - min_rating + 1
    x = np.linspace(min_rating, max_rating, M)
    N = len(scores)

    for i in range(N):
        Q = np.zeros(M)
        for w in scores[i].wins:
            Q += mmr.weight(scores[w[0] - 1].number_of_matches) * \
                 (mmr.logistic(np.abs(w[1])) *
                  mmr.win_distribution(x, scores[w[0] - 1].rating, scores[w[0] - 1].uncertainty, method=method) +
                  (1 - mmr.logistic(np.abs(w[1]))) *
                  mmr.loss_distribution(x, scores[w[0] - 1].rating, scores[w[0] - 1].uncertainty, method=method))
        for l in scores[i].losses:
            Q += mmr.weight(scores[l[0] - 1].number_of_matches) * \
                 (mmr.logistic(np.abs(l[1])) *
                  mmr.loss_distribution(x, scores[l[0] - 1].rating, scores[l[0] - 1].uncertainty, method=method) +
                  (1 - mmr.logistic(np.abs(l[1]))) *
                  mmr.win_distribution(x, scores[l[0] - 1].rating, scores[l[0] - 1].uncertainty, method=method))
        scores[i].performance = x[np.argmin(np.abs(Q))]
        if plot is True:
            plt.plot(x, Q, label=scores[i].first + ' ' + scores[i].last)
    return scores


def new_rating(competitor, match_uncert, stage_count, competitor_count, min_rating=rating_min, max_rating=rating_max, method=mmr_method, plot=False):
    """
    Calculates the performance ratings for all competitors

    Parameters
    ----------
    competitor : Competitor
        competitor with skill and performance rating
    match_uncert : float
        combined uncertainty for the entire match
    stage_count : int
        number of stages in match
    competitor_count : int
        number of competitors in division
    min_rating : int
        minimum rating
    max_rating : int
        maximum rating
    method : str
        normal: Gaussian distribution
        logistic: logistic distribution
    plot : bool
        Plot new Rating distribution

    Returns
    ----------
    competitor : Competitor
        updated competitor
    """

    M = max_rating - min_rating + 1
    x = np.linspace(min_rating, max_rating, M)
    skill = mmr.pdf(x, competitor.rating, competitor.uncertainty, method=method)
    perf = mmr.pdf(x, competitor.performance, match_uncert, method=method)
    rating_distribution = skill * perf
    delta = x[np.argmax(rating_distribution)] - competitor.rating

    w_stages = (mmr.logistic(stage_count - 1, scale=stage_count_factor) - 0.5) * 3 + 0.1
    w_competitors = (mmr.logistic(competitor_count - 1, scale=competitor_count_factor) - 0.5) * 3 + 0.1

    delta = np.mean([w_stages, w_competitors]) * delta
    competitor.rating = np.round(competitor.rating + delta, 0)
    competitor.last_change = np.round(delta,  0)
    if plot is True:
        plt.plot(x, rating_distribution, label=competitor.first + ' ' + competitor.last)
    return competitor


def match_uncertainty(scores):
    """
    Calculates the performance ratings for all competitors

    Parameters
    ----------
    scores : list
        list of Competitors at match

    Returns
    ----------
    uncertainty : float
        combined match
    """

    u_sqr = 0
    N = len(scores)
    for competitor in scores:
        u_sqr += competitor.uncertainty ** 2 / N

    return np.sqrt(u_sqr)


def new_uncertainty(scores, match_uncertainty):
    """
    Calculates the new rating uncertainty for all competitors

    Parameters
    ----------
    scores : list
        list of Competitors at match
    match_uncertainty : float
        combined uncertainty for the entire match

    Returns
    ----------
    scores : list
        original list with updated Competitor info
    """
    def pseudo_rms(u1, u2):
        return 0.5 * np.sqrt(u1 ** 2 + u2 ** 2)

    for competitor in scores:
        uncertainty = pseudo_rms(competitor.uncertainty, match_uncertainty)
        competitor.uncertainty = uncertainty
    return scores
