import flask
from flask import Flask, render_template, request, redirect, url_for
from app import app
from backend.login import *
from backend.account import *
from backend.field import *
from backend.crop import *
from backend.plant import *
from backend.harvest import *
from backend.check import *
from backend.basic_salary import *
from backend.salary import *
from backend.task import *
from backend.leave import *
from backend.statistics import *
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


@app.route("/password_change.html")
def change_password_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./password_change.html', user_id=user_id)


@app.route("/welcome_field.html")
def welcome_field_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./welcome_field.html', user_id=user_id)


@app.route("/check_in.html")
def check_in_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./check_in.html', user_id=user_id, role=role)


@app.route("/field_add.html")
def field_add_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./field_add.html', user_id=user_id)


@app.route("/field_info.html")
def field_info_html():
    field_id = request.args.get('field_id')
    return flask.render_template('./field_info.html', field_id=field_id)


@app.route("/field_change.html")
def field_change_html():
    field_id = request.args.get('field_id')
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./field_change.html', field_id=field_id, user_id=user_id, role=role)


@app.route("/employee.html")
def employee_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./employee.html', user_id=user_id, role=role)


@app.route("/employee_change.html")
def employee_change_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./employee_change.html', user_id=user_id, role=role)


@app.route("/crop.html")
def crop_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./crop.html', user_id=user_id, role=role)


@app.route("/crop_add.html")
def crop_add_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./crop_add.html', user_id=user_id, role=role)


@app.route("/crop_info.html")
def crop_info_html():
    crop_id = request.args.get('crop_id')
    return flask.render_template('./crop_info.html', crop_id=crop_id)


@app.route("/crop_change.html")
def crop_change_html():
    crop_id = request.args.get('crop_id')
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./crop_change.html', crop_id=crop_id, user_id=user_id, role=role)


@app.route("/plant.html")
def plant_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./plant.html', user_id=user_id, role=role)


@app.route("/plant_add.html")
def plant_add_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./plant_add.html', user_id=user_id, role=role)


@app.route("/plant_info.html")
def plant_info_html():
    crop_id = request.args.get('crop_id')
    field_id = request.args.get('field_id')
    return flask.render_template('./plant_info.html', crop_id=crop_id, field_id=field_id)


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


@app.route("/welcome_hr.html")
def welcome_hr_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./welcome_hr.html', user_id=user_id)


@app.route("/salary.html")
def salary_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./salary.html', user_id=user_id, role=role)


@app.route("/task.html")
def task_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./task.html', user_id=user_id, role=role)


@app.route("/task_add.html")
def task_add_html():
    return flask.render_template('./task_add.html')


@app.route("/task_change.html")
def task_change_html():
    task_id = request.args.get('task_id')
    return flask.render_template('./task_change.html', task_id=task_id)


@app.route("/welcome_plant.html")
def welcome_plant_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./welcome_plant.html', user_id=user_id)


@app.route("/welcome_harvest.html")
def welcome_harvest_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./welcome_harvest.html', user_id=user_id)


@app.route("/task_employee.html")
def task_employee_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./task_employee.html', user_id=user_id, role=role)


@app.route("/task_info.html")
def task_info_html():
    task_id = request.args.get('task_id')
    return flask.render_template('./task_info.html', task_id=task_id)


@app.route("/for_leave_request.html")
def for_leave_request_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./for_leave_request.html', user_id=user_id)


@app.route("/leave.html")
def leave_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./leave.html', user_id=user_id, role=role)


@app.route("/leave_change.html")
def leave_change_html():
    leave_id = request.args.get('leave_id')
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./leave_change.html', leave_id=leave_id, user_id=user_id, role=role)


@app.route("/leave_employee.html")
def leave_employee_html():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./leave_employee.html', user_id=user_id, role=role)


@app.route("/leave_info.html")
def leave_info_html():
    leave_id = request.args.get('leave_id')
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    return flask.render_template('./leave_info.html', leave_id=leave_id, user_id=user_id, role=role)


@app.route("/welcome_admin.html")
def welcome_admin_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./welcome_admin.html', user_id=user_id)


@app.route('/01.jpg')
def img01():
    return app.send_static_file('01.jpg')


if __name__ == '__main__':
    app.run(debug=True)
