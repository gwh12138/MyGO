from run import app
from flask import request, jsonify
import dbapi as db


@app.route('/field_list')
def get_field_list():
    """

    :return: {
        "field_class": field_class,
        "field_list": [
        {
            'field_id':field[0],
            'field_name':field[1],
            'field_pos':field[2],
            'size':field[3],
            'field_class':field[4],
            'field_outcome':field[5],
        },
        ...... ]
    }
    """
    field_class = request.args.get("field_class")
    field_id = request.args.get("field_id")
    if field_class is None and field_id is None:
        field_list = db.get_field_list()
        field_class = 'all'
        field_id = 0
    elif field_class is not None:
        field_id = 0
        field_list = db.get_field_class(field_class)
    else:
        field_class = 'all'
        field_list = db.get_field(field_id)
    resp = {
        "field_id": field_id,
        "field_class": field_class,
        "field_list": field_list,
    }

    return jsonify(resp)


@app.route('/change_field', methods=['POST'])
def change_field():
    field_id = request.json.get('field_id')
    field_name = request.json.get('field_name')
    field_pos = request.json.get('field_pos')
    size = request.json.get('field_size')
    field_class = request.json.get('field_class')
    field_outcome = request.json.get('field_outcome')
    if None in (field_id, field_name, field_pos, size, field_class, field_outcome):
        return jsonify({
            'response': 'None input'
        })

    res = db.change_field(field_id, field_name, field_pos, size, field_class, field_outcome)
    if res is None:
        return jsonify({
            'response': 'database false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'false'
        })


@app.route('/add_field', methods=['POST'])
def add_filed():
    field_name = request.form.get('field_name')
    field_pos = request.form.get('field_pos')
    size = request.form.get('field_size')
    field_class = request.form.get('field_class')
    field_outcome = request.form.get('field_outcome')
    if None in (field_name, field_pos, size, field_class, field_outcome):
        return jsonify({
            'response': 'None input'
        })
    res = db.add_field(field_name, field_pos, size, field_class, field_outcome)
    if res is None:
        return jsonify({
            'response': 'database false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'false'
        })


@app.route('/del_field')
def del_field():
    field_id = request.args.get('field_id')
    if field_id is None:
        return jsonify({
            'response': 'None input'
        })

    res = db.del_field(field_id)
    if res is None:
        return jsonify({
            'response': 'database false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'false'
        })


