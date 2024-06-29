from ..app import app
from flask import request, jsonify
from ..dbse import *


@app.route("/add_crop", methods=["POST"])
def add_field():
    field_name = request.json.get("field_name")
    size = request.json.get("size")
    crop_class = request.json.get("crop_class")
    latitude = request.json.get("latitude")
    longitude = request.json.get("longitude")
    N = request.json.get("N")
    P = request.json.get("P")
    K = request.json.get("K")
    pH = request.json.get("pH")
    length = request.json.get("length")
    width = request.json.get("width")
    if None in (field_name, size, crop_class, latitude, longitude, N, P, K, pH, length, width):
        return jsonify({
            'response': 'input none',
        })

    field_id = field.add_field(field_name, size, crop_class, latitude, longitude, N, P, K, pH, length, width)
    if field_id is None:
        return jsonify({
            'response': '500',
        })
    elif field_id == 0:
        return jsonify({
            'response': 'same name'
        })
    else:
        return jsonify({
            'response': 'success',
            'field_id': field_id
        })


@app.route("/del_field", methods=["POST"])
def del_field():
    field_id = request.json.get("field_id")
    if field_id is None:
        return jsonify({
            'response': 'input none',
        })

    res = field.del_field(field_id)
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


@app.route("/change_field", methods=["POST"])
def change_field():
    field_id = request.json.get("field_id")
    field_name = request.json.get("field_name")
    size = request.json.get("size")
    crop_class = request.json.get("crop_class")
    latitude = request.json.get("latitude")
    longitude = request.json.get("longitude")
    N = request.json.get("N")
    P = request.json.get("P")
    K = request.json.get("K")
    pH = request.json.get("pH")
    length = request.json.get("length")
    width = request.json.get("width")
    if field_id is None:
        return jsonify({
            'response': 'input none',
        })
    if field_name is None and size is None and crop_class is None and latitude is None and longitude is None and N is None and P is None and K is None and pH is None and length is None and width is None:
        return jsonify({
            'response': 'input none',
        })

    res = field.change_field(field_id, field_name, size, crop_class, latitude, longitude, N, P, K, pH, length, width)
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


@app.route("/search_field", methods=["POST"])
def search_field():
    field_id = request.json.get("field_id")
    field_name = request.json.get("field_name")
    size = request.json.get("size")
    crop_class = request.json.get("crop_class")
    latitude = request.json.get("latitude")
    longitude = request.json.get("longitude")
    N = request.json.get("N")
    P = request.json.get("P")
    K = request.json.get("K")
    pH = request.json.get("pH")
    length = request.json.get("length")
    width = request.json.get("width")

    res = field.search_field(field_id, field_name, size, crop_class, latitude, longitude, N, P, K, pH, length, width)
    resp = [{
        'field_id': re[0],
        'field_name': re[1],
        'size': re[2],
        'crop_class': re[3],
        'latitude =': re[4],
        'longitude': re[5],
        'N': re[6],
        'P': re[7],
        'K': re[8],
        'pH': re[9],
        'length': re[10],
        'width': re[11],
    } for re in res]
    return jsonify(resp)
