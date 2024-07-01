import csv
from app import app
from flask import request, jsonify
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
    res = employee_info.del_employee_info(user_id)
    if not res:
        return jsonify({
            'response': '500'
        })
    elif res == 0:
        return jsonify({
            'response': 'error user name or error password'
        })
    res = account.del_account(user_id, password)
    if not res:
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
        if not res:
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
    role = request.json.get("role")
    if sex or real_name:
        accounts = employee_info.search_employee_info(sex=sex)
        res = [list(account.search_account(acc[0])[0]) + list(acc[1:]) for acc in accounts]
    else:
        accounts = account.search_account(user_id, user_name, role)
        res = [list(acc) + list(employee_info.search_employee_info(acc[0])[0][1:]) for acc in accounts]
    res = {
        "account_list":
            [{"user_id": r[0],
              "user_name": r[1],
              "pwd": r[2],
              "role": r[3],
              "real_name": r[4],
              "sex": r[5],
              "telephone": r[6],
              "birthday": r[7],
              "work_experience": r[8],
              "profile": r[9],
              } for r in res]
    }
    return jsonify(res)


def output_account_csv(root):
    res = account.search_account()
    data = [list(re) + list(employee_info.search_employee_info(re[0])[0])[0:-1] for re in res]
    with open(root, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def input_account_csv(root):
    reader = csv.reader(root)
    for row in reader:
        user_id = account.add_account(row[0], row[1], row[2])
        employee_info.add_employee_info(user_id, row[3], row[4], row[5], row[6])