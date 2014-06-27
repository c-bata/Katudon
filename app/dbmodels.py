# coding : utf-8

import urllib2
from xml.etree.ElementTree import *
from app import db

def get_xml_string(TIMETABLE_URL):
    try:
        xmlString = urllib2.urlopen(TIMETABLE_URL).read()
    except urllib2.HTTPError as err:
        print('HTTPError')
        print(err)
    except urllib2.URLError as err:
        print('URLError')
        print(err)
        if isinstance(err.reason, socket.timeout):
            print('timeout')
    else:
        print('Get XML')

    return fromstring(xmlString)

def parse_xml():
    TIMETABLE_URL = "http://www.akashi.ac.jp/data/timetable/timetable201404.xml"
    element = get_xml_string(TIMETABLE_URL)

    #db.create_all()

    for elem1 in element[0][1]:
        timetable = User()
        for elem in elem1:
            if 'Name' in elem.tag:
                timetable.name = elem.text
            elif 'Grade' in elem.tag:
                timetable.name = elem.name
            elif 'Department' in elem.tag:
                timetable.department = elem.department
            elif 'Wday' in elem.tag:
                timetable.wday = elem.wday
            elif 'Location' in elem.tag:
                timetable.location = elem.location
            elif 'Uri' in elem.tag:
                timetable.uri = elem.uri
        db.session.add(timetable)
    db.session.commit()


class WeeklyMenu(db.Model):
    u"""week menu table."""
    __tablename__ = 'weeklymenus'
    week_id    = db.Column(db.Integer, primary_key=True)
    don        = db.Column(db.String(32))
    ramen      = db.Column(db.String(32))
    start_date = db.Column(db.DateTime)
    end_date   = db.Column(db.DateTime)

    def __init__(self, don, ramen, start_date, end_date):
        """ Initializes the fields with entered data """
        self.don        = don
        self.ramen      = ramen
        self.start_date = start_date
        self.end_date   = end_date

class DailyMenu(db.Model):
    u"""dayly menu table."""
    __tablename__ = 'dailymenus'
    id     = db.Column(db.String(16), primary_key=True)
    amenu  = db.Column(db.String(32))
    bmenu  = db.Column(db.String(32))
    date   = db.Column(db.DateTime)

    def __init__(self, amenu, bmenu, date):
        """ Initializes the fields with entered data """
        self.amenu = amenu
        self.bmenu = bmenu
        self.date  = date

class ClassTable(db.Model):
    u"""class table."""
    __tablename__ = 'classtables'
    classid    = db.Column(db.Integer, primary_key=True)
    classname  = db.Column(db.String(64))
    syllabus   = db.Column(db.String(64))

    def __init__(self, classname, syllabus):
        """ Initializes the fields with entered data """
        self.classname = classname
        self.syllabus  = syllabus

class StudentTable(db.Model):
    u"""student table."""
    __tablename__ = 'studenttables'
    classid = db.Column(db.Integer, primary_key=True)
    sex     = db.Column(db.Boolean)
    abroad  = db.Column(db.Boolean)

    def __init__(self, sex, abroad):
        """ Initializes the fields with entered data """
        self.sex    = sex
        self.abroad = abroad

class GradeTable(db.Model):
    u"""grade table."""
    __tablename__ = 'gradetables'
    id  = db.Column(db.Integer, primary_key=True)
    grade      = db.Column(db.Integer)
    department = db.Column(db.Integer) # 0:m, 1:e, 2:c, 3:a, 4:me ,5:ac
    cource     = db.Column(db.Boolean) # true: j, false:e
    wday       = db.Column(db.Integer) # 0:mon, 1:tue, ...
    sex        = db.Column(db.Boolean) # true: women only, false: men only
    abroad     = db.Column(db.Boolean) # true: abroad only, false:japanese only
    classid    = db.Column(db.Integer)

    def __init__(self, school_id, grade, department, cource, sex, abroad,
            classid):
        """ Initializes the fields with entered data """
        self.grade      = grade
        self.department = department
        self.cource     = cource
        self.sex        = sex
        self.abroad     = abroad
        self.classid    = classid

