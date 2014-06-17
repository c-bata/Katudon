#coding : utf-8

from flask import Flask, render_template, request, flash, session, redirect, url_for,g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.googleauth import (GoogleFederated, GoogleAuth)

app = Flask(__name__)
app.config.from_object('config')
auth = GoogleFederated('s.akashi.ac.jp', app)
db = SQLAlchemy(app)

from app import views, models

