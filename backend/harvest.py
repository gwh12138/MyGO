from app import app
from flask import request, jsonify
from dbse import *


@app.route('/add_harvest', methods=['POST'])
def add_harvest():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    harvest_date = request.json.get('harvest_date')
    harvest_weight = request.json.get('harvest_weight')
    if None in (field_id, crop_id, harvest_date):
        return jsonify({
            'response': 'input none'
        })
    if not harvest_weight:
        res = plant_info.search_plant_info(field_id, crop_id)
        if not res:
            return jsonify({
                'response': 'illegal harvest'
            })
        res = res[0]
        size = res[5]
        yield_per = crop.search_crop(crop_id=crop_id)[0][5]
        harvest_weight = size * yield_per

    res = harvest_info.add_harvest_info(field_id, crop_id, harvest_date, harvest_weight)
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


@app.route('/del_harvest', methods=['POST'])
def del_harvest():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    if None in (field_id, crop_id):
        return jsonify({
            'response': 'input none'
        })
    res = harvest_info.del_harvest_info(crop_id, field_id)
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


@app.route('/change_harvest', methods=['POST'])
def change_harvest():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    harvest_date = request.json.get('harvest_date')
    harvest_weight = request.json.get('harvest_weight')
    if None in (field_id, crop_id):
        return jsonify({
            'response': 'input none'
        })

    if not harvest_date and not harvest_weight:
        return jsonify({
            'response': 'input none',
        })

    res = harvest_info.change_harvest_info(
        field_id,
        crop_id,
        harvest_date=harvest_date,
        harvest_weight=harvest_weight
    )
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


@app.route('/search_harvest', methods=['POST'])
def search_harvest():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    field_name = request.json.get('field_name')
    crop_name = request.json.get('crop_name')
    harvest_date = request.json.get('harvest_date')
    harvest_weight = request.json.get('harvest_weight')
    res = harvest_info.search_harvest_info(
        field_id=field_id,
        crop_id=crop_id,
        harvest_date=harvest_date,
        harvest_weight=harvest_weight
    )
    if field_name:
        field_id = field.search_field(field_name=field_name)
        if not field_id:
            return jsonify({
                'response': 'illegal field'
            })
        field_id = field_id[0][0]
        res = [re for re in res if re[0] == field_id]
    if crop_name:
        crop_id = crop.search_crop(crop_name=crop_name)
        if not crop_id:
            return jsonify({
                'response': 'illegal field'
            })
        crop_id = crop_id[0][0]
        res = [re for re in res if re[1] == crop_id]
    resp = {
        'harvest_list': [{
            'field_id': re[0],
            'field_name': field.search_field(re[0])[0][1],
            'crop_id': re[1],
            'crop_name': crop.search_crop(re[1])[0][1],
            'harvest_date': None if re[2] is None else re[2].strftime('%Y-%m-%d'),
            'harvest_weight':re[3],
        } for re in res]
    }
    return jsonify(resp)
