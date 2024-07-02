from datetime import datetime
from app import app
from flask import request, jsonify
from dbse import *


@app.route("/add_salary", methods=["POST"])
def add_salary():
    salary_date = request.json.get("salary_date")
    if salary_date is None:
        return jsonify({
            'response': 'none input'
        })
    salary_date = datetime.fromisoformat(salary_date)
    salary_date = salary_date.strftime('%Y-%m')
    if salary.search_salary(salary_date=salary_date):
        return jsonify({
            'response': 'success'
        })

    accounts = account.search_account()
    salary_list = [
        [
            acc[0],
            basic_salary.search_basic_salary(role_name=acc[3])[0][1],
            len(check_in.search_check_in(user_id=acc[0])) * 1000,
        ]
        for acc in accounts]
    for ll in salary_list:
        salary.add_salary(ll[0], salary_date, ll[1], ll[2], int(ll[1]) + int(ll[2]))
    return jsonify({
        'response': 'success'
    })


@app.route("/del_salary", methods=["POST"])
def del_salary():
    user_id = request.json.get("user_id")
    salary_date = request.json.get("salary_date")
    if user_id is None or salary_date is None:
        return jsonify({
            'response': 'none input'
        })
    res = salary.del_salary(user_id, salary_date)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif not res:
        return jsonify({
            'response': 'not found'
        })
    return jsonify({
        'response': 'success'
    })


@app.route("/change_salary", methods=["POST"])
def change_salary():
    user_id = request.json.get("user_id")
    salary_date = request.json.get("salary_date")
    state = request.json.get("state")
    if user_id is None or salary_date is None or state is None:
        return jsonify({
            'response': 'none input'
        })
    salary_date = datetime.fromisoformat(salary_date).strftime('%Y-%m')
    res = salary.change_salary(user_id, salary_date, state=state)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif not res:
        return jsonify({
            'response': 'not found'
        })
    return jsonify({
        'response': 'success'
    })


@app.route("/search_salary", methods=["POST"])
def search_salary():
    salary_date = request.json.get("salary_date")
    if salary_date:
        salary_date = datetime.fromisoformat(salary_date)
        salary_date = salary_date.strftime('%Y-%m')
    res = salary.search_salary(salary_date=salary_date)
    if res is None:
        return jsonify({
            'response': '500',
        })

    resp = {
        'salary_list': [{
            'user_id': re[0],
            'real_name': employee_info.search_employee_info(re[0])[0][1],
            'salary_date': re[1],
            'basic_salary': re[2],
            'performance_based_salary': re[3],
            'total_salary': re[4],
            'state': re[5],
        } for re in res]
    }
    return jsonify(resp)
