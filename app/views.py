#coding:utf-8

from flask import Flask, render_template, request, flash, session, redirect, url_for,g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.googleauth import (GoogleFederated, GoogleAuth)
from app import app, auth
from models import *
from models.user_predict import *


@app.route('/create_account', methods=['GET', 'POST'])
@auth.required
def create_account():
    """create a user account"""
    if request.method == 'POST':
        flash(u'フィールドに値を入力して下さい.', 'error')
        return render_template('create_account.html')
    else:
        return render_template('create_account.html')




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
    flash(u'Success to login! Welcome!' )
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
