from app import app
from flask import request, jsonify
from dbse import *
from datetime import datetime
import pytz


@app.route("/add_leave", methods=["POST"])
def add_leave():
    user_id = request.json.get("user_id")
    leave_state = request.json.get("leave_state")
    leave_date = request.json.get("leave_date")
    reason = request.json.get("reason")
    if None in (user_id, leave_date):
        return jsonify({
            'response': 'input none'
        })

    leave_date = datetime.fromisoformat(leave_date)
    local_timezone = pytz.timezone('Asia/Shanghai')
    leave_date = leave_date.astimezone(local_timezone)
    leave_id = leave.add_leave(user_id, leave_state, leave_date, reason)
    if leave_id is None:
        return jsonify({
            'response': '500',
        })
    elif leave_id == 0:
        return jsonify({
            'response': 'same name'
        })
    else:
        return jsonify({
            'response': 'success',
        })


@app.route("/del_leave", methods=["POST"])
def del_leave():
    leave_id = request.json.get("leave_id")
    res = leave.del_leave(leave_id)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif res == 0:
        return jsonify({
            'response': 'failure'
        })
    else:
        return jsonify({
            'response': 'success'
        })


@app.route("/change_leave", methods=["POST"])
def change_leave():
    leave_id = request.json.get("leave_id")
    user_id = request.json.get("user_id")
    leave_state = request.json.get("leave_state")
    leave_date = request.json.get("leave_date")
    reason = request.json.get("reason")
    if leave_id is None:
        return jsonify({
            'response': 'input none'
        })

    if leave_date:
        leave_date = datetime.fromisoformat(leave_date)
        local_timezone = pytz.timezone('Asia/Shanghai')
        leave_date = leave_date.astimezone(local_timezone)

    res = leave.change_leave(leave_id, user_id, leave_state, leave_date, reason)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif res == 0:
        return jsonify({
            'response': 'failure'
        })
    else:
        return jsonify({
            'response': 'success'
        })


@app.route("/search_leave", methods=["POST"])
def search_leave():
    leave_id = request.json.get("leave_id")
    user_id = request.json.get("user_id")
    leave_state = request.json.get("leave_state")
    leave_date = request.json.get("leave_date")
    res = leave.search_leave(leave_id, user_id, leave_state, leave_date)
    resp = {
        'leave_list': [{
            'leave_id': re[0],
            'user_id': re[1],
            'real_name': employee_info.search_employee_info(user_id=re[1])[0][1],
            'leave_state': re[2],
            'leave_date': None if re[3] is None else re[3].strftime('%Y-%m-%d'),
            'reason': re[4],
            'image_url': f'/image/{re[2]}',
        } for re in res]
    }
    return resp


@app.route("/image/<state>")
def leave_img(state):
    if state == u'申请中':
        return app.send_static_file('leave2.png')
    elif state == u'同意':
        return app.send_static_file('leave3.png')
    else:
        return app.send_static_file('leave1.png')


