from config import *
from Utilities import filehandler
from Application import rating


def get_competitor_rating(competitor, file=ratings_db):
    """
    Checks if a member is in the database, returns most recent rating info

    Parameters
    ----------
    competitor : rating.Competitor
        USPSA member number
    division : str
        Name of competitor's division
    match_type : str
        Type of match
    file : float
        file path to .db file

    Returns
    -------
    competitor : rating.Competitor
        Updated with rating info. If there is no entry for a competitor, returns FALSE
    """

    try:
        competitor.member.upper()
    except AttributeError:
        competitor.noob = True
        competitor.number_of_matches = 0
        competitor.rating = noob_skill
        competitor.uncertainty = noob_uncertainty
        return competitor
    else:
        try:
            (cursor, conn) = filehandler.open_database(file)
        except FileNotFoundError:
            raise FileNotFoundError
        except sqlite3.InterfaceError:
            raise FileNotFoundError

        sql = '''SELECT rating, uncertainty, match_count FROM ratings
                    WHERE UPPER(uspsa_number)=? AND division=? AND match_type=?
                    ORDER BY match_date_unix DESC
                    LIMIT 1'''
        cursor.execute(sql, (competitor.member.upper(), competitor.division, competitor.match_type))

        try:
            data = cursor.fetchall()
        except:
            filehandler.close_database(cursor, conn)
            raise IndexError('DATABASE: Read error.')

        if not data:
            filehandler.close_database(cursor, conn)
            competitor.noob = True
            competitor.number_of_matches = 0
            competitor.rating = noob_skill
            competitor.uncertainty = noob_uncertainty
            return competitor

    competitor.noob = False
    competitor.rating = data[0][0]
    competitor.uncertainty = data[0][1]

    if data[0][2] is None or data[0][2] == '':
        competitor.number_of_matches = 0
    else:
        competitor.number_of_matches = data[0][2]

    filehandler.close_database(cursor, conn)
    return competitor


def get_competitor_all(member_number, division, match_type='Pistol', file=ratings_db):
    """
    Checks if a member is in the database, returns most recent competitor info

    Parameters
    ----------
    member_number : str
        USPSA member number
    division : str
        Name of competitor's division
    match_type : str
        Type of match
    file : float
        file path to .db file

    Returns
    -------
    competitor : rating.Competitor
        All Competitor info. If there is no entry for a competitor, returns FALSE
    """

    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT * FROM ratings
             WHERE UPPER(uspsa_number)=? AND division=? AND match_type=?
             ORDER BY match_date_unix DESC
             LIMIT 1'''
    cursor.execute(sql, (member_number.upper(), division, match_type))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')

    if not data:
        filehandler.close_database(cursor, conn)
        return False

    ## Get Column info
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''PRAGMA table_info(ratings)'''
    cursor.execute(sql)

    try:
        columns = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')
    else:
        filehandler.close_database(cursor, conn)

    competitor = rating.Competitor()

    data = data[0]
    for column in columns:
        if column[1] == 'first':
            competitor.first = data[column[0]]
        if column[1] == 'last':
            competitor.last = data[column[0]]
        if column[1] == 'uspsa_number':
            competitor.member = data[column[0]]
        if column[1] == 'division':
            competitor.division = data[column[0]]
        if column[1] == 'rating':
            competitor.rating = data[column[0]]
        if column[1] == 'uncertainty':
            competitor.performance = data[column[0]]
        if column[1] == 'performance':
            competitor.uncertainty = data[column[0]]
        if column[1] == 'match_count':
            competitor.number_of_matches = data[column[0]]
        if column[1] == 'match_id':
            competitor.match_id = data[column[0]]
        if column[1] == 'club':
            competitor.club = data[column[0]]
        if column[1] == 'club_code':
            competitor.club_code = data[column[0]]
        if column[1] == 'match_type':
            competitor.match_type = data[column[0]]
        if column[1] == 'match_date':
            competitor.match_date = data[column[0]]
        if column[1] == 'match_date_unix':
            competitor.match_date_unix = data[column[0]]
    return competitor


def write_competitor(competitor, file=ratings_db):
    """
    Writes a competitor's info to the database as a new entry

    Parameters
    -------
    competitor : rating.Competitor
        Competitor info.
    file : float
        file path to .db file
    """
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    cursor = conn.cursor()
    sql = '''INSERT INTO ratings(first,last,uspsa_number,match_type,division,rating,last_change,uncertainty,performance,
                                 match_count,percent,match_id,match_name,club,club_code,match_date,match_date_unix)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    line = tuple([competitor.first, competitor.last, competitor.member, competitor.match_type, competitor.division,
                  competitor.rating, competitor.last_change, competitor.uncertainty, competitor.performance,
                  competitor.number_of_matches, competitor.percent, competitor.match_id, competitor.match_name,
                  competitor.club, competitor.club_code, competitor.match_date, competitor.match_date_unix])
    cursor.execute(sql, line)
    conn.commit()

    filehandler.close_database(cursor, conn)


def get_classifier_codes(file=classifiers_db):
    """
    Reads the classifier codes in the database

    Parameters
    -------
    file : float
        file path to .db file
    """
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT DISTINCT classifier_code FROM match_scores
             ORDER BY classifier_code ASC'''
    cursor.execute(sql, )

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')

    filehandler.close_database(cursor, conn)
    return data


def get_classifier_scores(code, division, file=classifiers_db):
    """
    Reads the classifier codes in the database

    Parameters
    -------
    code : str
        classifier code
    division : str
        division name
    file : str
        file path to .db file

    Returns
    -------
    data : list
        list of classifier scores [(member_number, hitfactor, date_unix)]
    """
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT member_number, hitfactor, date_unix FROM match_scores
             WHERE classifier_code=? AND division=?
             ORDER BY date_unix ASC
             LIMIT 10'''
    cursor.execute(sql, (code, division))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')

    filehandler.close_database(cursor, conn)
    return data


def get_unique_competitors(division='Carry Optics', file=ratings_db):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT DISTINCT uspsa_number FROM ratings
             WHERE division=?'''
    cursor.execute(sql, (division, ))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')

    filehandler.close_database(cursor, conn)
    return data


def get_competitor_history(member, division='Carry Optics', file=ratings_db):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT first, last, rating, uncertainty, performance, match_date_unix FROM ratings
             WHERE uspsa_number=? AND division=?'''
    cursor.execute(sql, (member, division))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')

    filehandler.close_database(cursor, conn)
    return data


def get_competitor_current(member, division='Carry Optics', min_matches=3, file=ratings_db):
    try:
        (cursor, conn) = filehandler.open_database(file)
    except FileNotFoundError:
        raise FileNotFoundError
    except sqlite3.InterfaceError:
        raise FileNotFoundError

    sql = '''SELECT first, last, rating, last_change, uncertainty, performance, match_date_unix, match_count FROM ratings
             WHERE uspsa_number=? AND division=?
             ORDER BY match_date_unix DESC
             LIMIT 1'''
    cursor.execute(sql, (member, division))

    try:
        data = cursor.fetchall()
    except:
        filehandler.close_database(cursor, conn)
        raise IndexError('DATABASE: Read error.')

    filehandler.close_database(cursor, conn)

    if data[0][7] <= min_matches:
        return None
    return data
