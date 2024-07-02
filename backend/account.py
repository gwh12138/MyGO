import csv
from app import app
from flask import request, jsonify, send_file
from dbse import *


@app.route("/add_account", methods=["POST"])
def add_account():
    user_name = request.json.get("user_name")
    password = request.json.get("pwd")
    role = request.json.get("role")
    real_name = request.json.get("real_name")
    sex = request.json.get("sex")
    telephone = request.json.get("telephone")
    birthday = request.json.get("birthday")
    work_experience = request.json.get("work_experience")
    profile = request.json.get("profile")

    res = account.add_account(user_name, password, role)
    if not res:
        return jsonify({
            'response': '500'
        })
    elif res == 0:
        return jsonify({
            'response': 'same name'
        })

    employee_info.add_employee_info(user_id=res, real_name=real_name, sex=sex, telephone=telephone, birthday=birthday,
                                    work_experience=work_experience, profile=profile)
    return None


@app.route("/del_account", methods=["POST"])
def del_account():
    user_id = request.json.get("user_id")
    password = request.json.get("pwd")
    if None in (user_id, password):
        return jsonify({
            'response': 'input none'
        })
    _password = account.search_account(user_id)
    if _password is None:
        return jsonify({
            'response': '500'
        })
    elif _password == 0:
        return jsonify({
            'response': 'error user id'
        })
    _password = _password[0][2]
    if _password != password:
        return jsonify({
            'response': 'error password'
        })

    res = account.del_account(user_id)
    if res is None:
        return jsonify({
            'response': '500'
        })
    elif res == 0:
        return jsonify({
            'response': 'error user name or error password'
        })
    else:
        return jsonify({
            'response': 'success'
        })


@app.route("/change_account", methods=["POST"])
def change_account():
    user_id = request.json.get("user_id")
    user_name = request.json.get("user_name")
    password = request.json.get("pwd")
    role = request.json.get("role")
    sex = request.json.get("sex")
    real_name = request.json.get("real_name")
    telephone = request.json.get("telephone")
    birthday = request.json.get("birthday")
    work_experience = request.json.get("work_experience")
    profile = request.json.get("profile")

    if not user_id:
        return jsonify({
            'response': 'user id none'
        })
    if user_name is not None or password is not None or role is not None:
        res = account.change_account(user_id=user_id,
                                     user_name=user_name,
                                     password=password,
                                     role=role)
        if res is None:
            return jsonify({
                'response': 'same name'
            })
    if real_name is not None or telephone is not None or birthday is not None or work_experience is not None or profile is not None or sex is not None:
        employee_info.change_employee_info(user_id, real_name, sex, telephone, birthday, work_experience, profile)
    return jsonify({
        'response': 'success'
    })


@app.route("/search_account", methods=["POST"])
def search_account():
    user_id = request.json.get("user_id")
    user_name = request.json.get("user_name")
    real_name = request.json.get("real_name")
    sex = request.json.get("sex")
    telephone = request.json.get("telephone")
    birthday = request.json.get("birthday")
    role = request.json.get("role")
    accounts = account.search_account(user_id, user_name, role)
    res = [list(acc) + list(employee_info.search_employee_info(acc[0])[0][1:]) for acc in accounts]
    if sex or real_name or telephone or birthday:
        employee = employee_info.search_employee_info(sex=sex,
                                                      real_name=real_name,
                                                      telephone=telephone,
                                                      birthday=birthday)
        employee = [list(account.search_account(acc[0])[0]) + list(acc[1:]) for acc in employee]
        res = [acc for acc in employee if acc in res]

    res = {
        "account_list":
            [{"user_id": r[0],
              "user_name": r[1],
              "pwd": r[2],
              "role": r[3],
              "real_name": r[4],
              "sex": r[5],
              "telephone": r[6],
              "birthday": None if r[7] is None else r[7].strftime('%Y-%m-%d'),
              "work_experience": r[8],
              "profile": r[9],
              } for r in res]
    }
    return jsonify(res)


@app.route('/input_account_csv', methods=["POST"])
def input_account_csv():
    file = request.files.get('file')
    root = './static/input.csv'
    file.save(root)
    with open(root, 'r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    for row in data:
        if len(row) != 10:
            return jsonify({
                'response': 'illegal format'
            })
    for row in data:
        user_id = account.add_account(row[1], row[2], row[3])
        employee_info.add_employee_info(user_id, row[4], row[5], row[6], row[7], row[8])
    return jsonify({
        'response': 'success'
    })


@app.route('/output_account_csv', methods=["POST"])
def output_account_csv():
    accounts = account.search_account()
    res = [list(acc) + list(employee_info.search_employee_info(acc[0])[0][1:]) for acc in accounts]
    root = './static/information.csv'
    with open(root, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(res)
    return send_file(root)
