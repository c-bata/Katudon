#coding:utf-8

from flask import Flask, render_template, request, flash, session, redirect, url_for,g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.googleauth import (GoogleFederated, GoogleAuth)
from app import app, auth, db
from dbmodels import *
from models.user_predict import *

@app.before_first_request
def init():
    db.drop_all() # 都合上起動する度にdbは削除. 本番環境に入れる前に消すこと！
    db.create_all()

class Users(db.Model):
    u"""user table
    courceの綴り間違えてるけど、直したら動かなくなったからこのままいく.
    はまりそうだからきをつけて"""
    __tablename__ = 'users'
    id         = db.Column('student_id', db.Integer, primary_key=True)
    school_id  = db.Column(db.String(16))
    grade      = db.Column(db.Integer)
    department = db.Column(db.Integer) # 0:m, 1:e, 2:c, 3:a, 4:me ,5:ac
    cource     = db.Column(db.Boolean) # true: j, false:e
    sex        = db.Column(db.Boolean) # true: women only, false: men only
    abroad     = db.Column(db.Boolean) # true: abroad only, false:japanese only

    def __init__(self, school_id, grade, department, cource, sex, abroad):
        """ Initializes the fields with entered data """
        self.school_id  = school_id
        self.grade      = grade
        self.department = department
        self.cource     = cource
        self.sex        = sex
        self.abroad     = abroad


@app.route('/create_account', methods=['GET', 'POST'])
@auth.required
def create_account():
    """create a user account"""
    if request.method == 'POST':

        # POST REQUEST

        ## request.form['grade']等が存在しないからif文でも呼び出すだけでBadRequest
        ## が帰る.
        #if not request.form['grade'] \
        #or not request.form['department'] \
        #or not request.form['course'] \
        #or not request.form['sex']:

        if request.form['grade'] == u'' \
                or request.form['department'] == u'':

            flash(u'Please enter all the fields.', 'error')
            return render_template('create_account.html')
        else:

            if request.form.get('course') == u'elec':
                course = True
            else:
                course = False
            if request.form.get('sex') == u'female':
                sex = True
            else:
                sex = False
            if request.form.get('abroad') is None:
                abroad = False
            else:
                abroad = True

            get_department = request.form['department']
            department = 1 # ミスってた時のためにE科で初期化.
            if get_department == u'M':
                department = 0
            elif get_department == u'E':
                department = 1
            elif get_department == u'C':
                department = 2
            elif get_department == u'A':
                department = 3
            elif get_department == u'ME':
                department = 4
            elif get_department == u'AC':
                department = 5

            user = Users(get_school_id_from_mail_adress(g.user['email']),
                        int(request.form['grade']),
                        department,
                        course,
                        sex,
                        abroad)


            db.session.add(user)
            db.session.commit()
            flash('Your account was successfully created')
            return redirect(url_for('home'))
    else:
        # GET REQUEST
        user_info = predict_user_info(g.user['email'])
        # userinfo["department"] or userinfo["grade"]みたいに使う.
        return render_template('create_account.html',
                userinfo = user_info)


@app.route('/')
@app.route('/index')
def index():
    """Return index.html"""
    return render_template('index.html')

@app.route('/home')
@auth.required
def home():
    u"""
    Show TimeTable & Lunch Menu
    もしユーザテーブルにそのメールアドレスがなかったらcreate_accountにredirect
    """

    user = db.session.query(Users).filter(Users.school_id == \
            get_school_id_from_mail_adress(g.user['email'])).first()

    if user == None:
        flash(u'アカウントを作成して下さい.')
        return redirect(url_for('create_account'))

    import pdb;pdb.set_trace()

    timetable = [{"name":u"一限目","uri":"http://google.co.jp"},
            {"name":u"二限目","uri":"http://yahoo.co.jp"},
            {"name":u"三限目","uri":"http://youtube.com"}]
    timetable.append({"name":u"四限目","uri":"http://b.hatena.ne.jp"})

    school_lunch = [u'Aセット', u'Bセット', u'週替り丼', u'とんこつラーメン']

    return render_template('home.html',
            timetables = timetable,
            lunchs = school_lunch)

@app.route('/login_route')
def login_route():
    u"""
    Login. homeにauth.requiredつけてるけど、
    そこでflashつけるとホームに戻る度に
    ログイン成功メッセージが表示されてしまう.
    """
    auth._login()
    #flash(u'ログインに成功しました. ようこそ！%s %sさん' % (g.user['last_name'], g.user['first_name']) )
    #flash(u'Success to login! Welcome!' )
    return redirect(url_for('home'))

@app.route('/logout_route')
def logout_route():
    """Logout"""
    auth._logout()
    flash(u'ログアウトしました.' )
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('404.html')
    #return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def error_occured(e):
    """Return a custom 500 error."""
    return render_template('error.html')
    #return 'Sorry, unexpected error: {}'.format(e), 500
