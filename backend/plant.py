from app import app
from flask import request, jsonify
from dbse import *


@app.route('/add_plant', methods=['POST'])
def add_plant():
    field_name = request.json.get('field_name')
    crop_name = request.json.get('crop_name')
    plant_date = request.json.get('plant_date')
    crop_state = request.json.get('crop_state')
    irrigation = request.json.get('irrigation')
    size = request.json.get('size')
    longitude = request.json.get('longitude')
    latitude = request.json.get('latitude')
    if None in (field_name, crop_name, plant_date, size, longitude, latitude):
        return jsonify({
            'response': 'input none'
        })
    field_id = field.search_field(field_name=field_name)
    crop_id = crop.search_crop(crop_name=crop_name)
    if not field_id or not crop_id:
        return jsonify({
            'response': 'illegal name'
        })
    field_id = field_id[0][0]
    crop_id = crop_id[0][0]
    res = plant_info.add_plant_info(field_id, crop_id, plant_date, crop_state, irrigation, size, longitude, latitude)
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


@app.route('/del_plant', methods=['POST'])
def del_plant():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    if None in (field_id, crop_id):
        return jsonify({
            'response': 'input none'
        })
    res = plant_info.del_plant_info(field_id, crop_id)
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


@app.route('/change_plant', methods=['POST'])
def change_plant():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    plant_date = request.json.get('plant_date')
    crop_state = request.json.get('crop_state')
    irrigation = request.json.get('irrigation')
    size = request.json.get('size')
    longitude = request.json.get('longitude')
    latitude = request.json.get('latitude')
    if None in (field_id, crop_id):
        return jsonify({
            'response': 'input none'
        })

    if not plant_date and not crop_state and not irrigation and not size and not longitude and not latitude:
        return jsonify({
            'response': 'input none',
        })

    res = plant_info.change_plant_info(field_id,
                                       crop_id,
                                       plant_date=plant_date,
                                       crop_state=crop_state,
                                       irrigation=irrigation,
                                       size=size,
                                       longitude=longitude,
                                       latitude=latitude)
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


@app.route('/search_plant', methods=['POST'])
def search_plant():
    field_id = request.json.get('field_id')
    crop_id = request.json.get('crop_id')
    field_name = request.json.get('field_name')
    crop_name = request.json.get('crop_name')
    plant_date = request.json.get('plant_date')
    crop_state = request.json.get('crop_state')
    irrigation = request.json.get('irrigation')
    size = request.json.get('size')
    longitude = request.json.get('longitude')
    latitude = request.json.get('latitude')

    res = plant_info.search_plant_info(field_id,
                                       crop_id,
                                       plant_date=plant_date,
                                       crop_state=crop_state,
                                       irrigation=irrigation,
                                       size=size,
                                       longitude=longitude,
                                       latitude=latitude)
    res = [list(field.search_field(re[0])[0])[0:2] + list(crop.search_crop(re[1])[0])[0:2] + list(re[2:]) for re in res]
    if field_name:
        res = [re for re in res if re[1] == field_name]
    if crop_name:
        res = [re for re in res if re[3] == crop_name]

    resp = {
        'plant_list': [{
            'field_id': re[0],
            'field_name': re[1],
            'crop_id': re[2],
            'crop_name': re[3],
            'plant_date': None if re[4] is None else re[4].strftime('%Y-%m-%d'),
            'crop_state': re[5],
            'irrigation': re[6],
            'size': re[7],
            'longitude': re[8],
            'latitude': re[9],
        } for re in res]
    }
    return jsonify(resp)

