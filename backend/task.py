from app import app
from flask import request, jsonify
from dbse import *
from datetime import datetime
import pytz


@app.route("/add_task", methods=["POST"])
def add_task():
    user_id = request.json.get("user_id")
    operate = request.json.get("operate")
    crop_name = request.json.get("crop_name")
    field_name = request.json.get("field_name")
    description = request.json.get("description")
    complete_time = request.json.get("complete_time")
    task_state = request.json.get("task_state")
    crop_id = None
    field_id = None
    if None in (operate, description):
        return jsonify({
            'response': 'input none'
        })
    if crop_name:
        crop_id = crop.search_crop(crop_name=crop_name)
        if not crop_id:
            return jsonify({
                'response': 'illegal crop name'
            })
        crop_id = crop_id[0][0]
    if field_name:
        field_id = field.search_field(field_name=field_name)
        if not field_id:
            return jsonify({
                'response': 'illegal field name'
            })
        field_id = field_id[0][0]
    if complete_time:
        complete_time = datetime.fromisoformat(complete_time)
        local_timezone = pytz.timezone('Asia/Shanghai')
        complete_time = complete_time.astimezone(local_timezone)
    res = task.add_task(operate, crop_id, field_id, user_id, description, complete_time, task_state)
    if res is None:
        return jsonify({
            'response': '500',
        })
    elif res == 0:
        return jsonify({
            'response': 'same name'
        })
    else:
        return jsonify({
            'response': 'success',
        })


@app.route("/del_task", methods=["POST"])
def del_task():
    task_id = request.json.get("task_id")
    res = task.del_task(task_id)
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


@app.route("/change_task", methods=["POST"])
def change_task():
    task_id = request.json.get("task_id")
    user_id = request.json.get("user_id")
    operate = request.json.get("operate")
    crop_name = request.json.get("crop_name")
    field_name = request.json.get("field_name")
    description = request.json.get("description")
    task_state = request.json.get("task_state")
    complete_time = request.json.get("complete_time")
    crop_id = None
    field_id = None
    if crop_name:
        crop_id = crop.search_crop(crop_name=crop_name)
        if not crop_id:
            return jsonify({
                'response': 'illegal crop name'
            })
        crop_id = crop_id[0][0]
    if field_name:
        field_id = field.search_field(field_name=field_name)
        if not field_id:
            return jsonify({
                'response': 'illegal field name'
            })
        field_id = field_id[0][0]
    if complete_time:
        complete_time = datetime.fromisoformat(complete_time)
        local_timezone = pytz.timezone('Asia/Shanghai')
        complete_time = complete_time.astimezone(local_timezone)
    res = task.change_task(task_id, operate, crop_id, field_id, user_id, description, complete_time, task_state)
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


@app.route("/search_task", methods=["POST"])
def search_task():
    task_id = request.json.get("task_id")
    user_id = request.json.get("user_id")
    operate = request.json.get("operate")
    crop_name = request.json.get("crop_name")
    field_name = request.json.get("field_name")
    description = request.json.get("description")
    task_state = request.json.get("task_state")
    complete_time = request.json.get("complete_time")
    crop_id = None
    field_id = None
    if crop_name:
        crop_id = crop.search_crop(crop_name=crop_name)
        if not crop_id:
            return jsonify({
                'response': 'illegal crop name'
            })
        crop_id = crop_id[0][0]
    if field_name:
        field_id = field.search_field(field_name=field_name)
        if not field_id:
            return jsonify({
                'response': 'illegal field name'
            })
        field_id = field_id[0][0]
    if complete_time:
        complete_time = datetime.fromisoformat(complete_time)
        local_timezone = pytz.timezone('Asia/Shanghai')
        complete_time = complete_time.astimezone(local_timezone)
    res = task.search_task(task_id, operate, crop_id, field_id, user_id, description, complete_time, task_state)
    resp = {
        'task_list': [{
            'task_id': re[0],
            'operate': re[1],
            'crop_id': re[2],
            'field_id': re[3],
            'user_id': re[4],
            'description': re[5],
            'complete_time': re[6],
            'task_state': re[7],
            'crop_name': crop.search_crop(crop_id=re[2])[0][1],
            'field_name': field.search_field(field_id=re[3])[0][1],
        } for re in res]
    }
    return jsonify(resp)

