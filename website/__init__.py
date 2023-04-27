from flask import Flask
from flask import Blueprint, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from functools import wraps
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .authenticate import authenticate
    from .order import order

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(authenticate, url_prefix='/')
    app.register_blueprint(order, url_prefix='/')
    return app





def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')