# coding: utf-8
import re
import datetime

def is_email_adress_valid(email):
    """
    Validate school email adress using regular expression.

    >>> is_email_adress_valid("e1020@s.akashi.ac.jp")
    True
    >>> is_email_adress_valid("ac1020@akashi.ac.jp")
    True
    >>> is_email_adress_valid("1020@s.akashi.ac.jp")
    False
    >>> is_email_adress_valid("e020@s.akashi.ac.jp")
    False
    """

    if not re.match("[meca]{1,2}[0-9]{4}@(s\.)?akashi\.ac\.jp", email):
        return False
    return True

def get_school_id_from_mail_adress(email):
    """
    Get school id from email adress.

    >>> get_school_id_from_mail_adress("e1020@s.akashi.ac.jp")
    'e1020'
    >>> get_school_id_from_mail_adress("ac1020@akashi.ac.jp")
    'ac1020'
    >>> get_school_id_from_mail_adress("1020@s.akashi.ac.jp")
    '1020'
    >>> get_school_id_from_mail_adress("e1020")
    'e1020'
    """
    return email.split('@')[0]

def predict_user_info(email):
    """
    Predict user department and grade from email adress.
    Returned by dictionary type.

    - Usage
    user_info = predict_user_info("EMAIL_ADDRESS")
    print user_info["department"]
    print user_info["grade"]

    >>> predict_user_info("me0920@s.akashi.ac.jp") == {"department":"me","grade":1}
    True
    >>> predict_user_info("ac0801@s.akashi.ac.jp") == {"department":"ac","grade":2}
    True
    >>> predict_user_info("e1001@s.akashi.ac.jp")  == {"department":"e","grade":5}
    True
    >>> predict_user_info("c1401@s.akashi.ac.jp")  == {"department":"c","grade":1}
    True
    >>> predict_user_info("c0801@s.akashi.ac.jp")  == {"department":"c","grade":5}
    True
    """

    department = re.search('^[meca]{1,2}', email)
    year       = re.search('[0-9]{4}', email)
    d = datetime.datetime.today()

    year_sub = d.year -2000 - int(year.group(0)[:2])

    if d.month >= 1 and d.month <= 3:
        year_sub -= 1

    if len(department.group(0)) == 1:
        # ex) m, e, a, c -> regular cources student
        if year_sub >= 4:
            grade = 5
        elif year_sub >= 0:
            grade = year_sub + 1
        else:
            grade = 1

    else:
        # ex) me, ac -> advanced cources student
        if year_sub == 6:
            grade = 2
        else:
            grade = 1

    return {'department':department.group(0),'grade':grade}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
