import flask
from flask import Flask, render_template, request, redirect, url_for
from app import app
from backend.login import *
import dbse


@app.route("/")
def index():
    return flask.render_template('./login.html')


@app.route("/index.html")
def index_html():
    user_id = request.args.get('user_id')
    (user_id, user_name, password, role) = dbse.account.search_account(user_id=user_id)[0]
    return render_template('./index.html', user_id=user_id, user_name=user_name, role=role)


@app.route("/welcome.html")
def welcome_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./welcome.html', user_id=user_id)


@app.route("/user_info.html")
def user_info_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./user_info.html', user_id=user_id)


@app.route("/login.html")
def login_html():
    return flask.render_template('./login.html')


@app.route("/employee.html")
def employee_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./employee.html', user_id=user_id, role=role)


@app.route("/crop.html")
def crop_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./crop.html', user_id=user_id, role=role)


@app.route("/plant.html")
def plant_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./plant.html', user_id=user_id, role=role)


@app.route("/field.html")
def field_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./field.html', user_id=user_id, role=role)


@app.route("/harvest.html")
def harvest_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./harvest.html', user_id=user_id, role=role)


@app.route('/01.jpg')
def img01():
    return app.send_static_file('01.jpg')


if __name__ == '__main__':
    app.run(debug=True)
