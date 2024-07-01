from app import app
from flask import request, jsonify
from dbse import *


@app.route("/add_crop", methods=["POST"])
def add_crop():
    crop_name = request.json.get("crop_name")
    crop_class = request.json.get("crop_class")
    irrigation_per = request.json.get("irrigation_per")
    birth_cycle = request.json.get("birth_cycle")
    yield_per = request.json.get("yield_per")
    if None in (crop_name, crop_class, irrigation_per, birth_cycle, yield_per):
        return jsonify({
            'response': 'input none',
        })
    crop_id = crop.add_crop(crop_name, crop_class, irrigation_per, birth_cycle, yield_per)
    if crop_id is None:
        return jsonify({
            'response': '500',
        })
    elif crop_id == 0:
        return jsonify({
            'response': 'same name'
        })
    else:
        return jsonify({
            'response': 'success',
            'crop_id': crop_id
        })


@app.route("/del_crop", methods=["POST"])
def del_crop():
    crop_id = request.json.get("crop_id")
    if crop_id is None:
        return jsonify({
            'response': 'input none',
        })

    res = crop.del_crop(crop_id)
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


@app.route("/change_crop", methods=["POST"])
def change_crop():
    crop_id = request.json.get("crop_id")
    crop_name = request.json.get("crop_name")
    crop_class = request.json.get("crop_class")
    irrigation_per = request.json.get("irrigation_per")
    birth_cycle = request.json.get("birth_cycle")
    yield_per = request.json.get("yield_per")
    if crop_id is None:
        return jsonify({
            'response': 'crop_id none',
        })

    res = crop.change_crop(crop_id, crop_name, crop_class, irrigation_per, birth_cycle, yield_per)
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


@app.route("/search_crop", methods=["POST"])
def search_crop():
    crop_id = request.json.get("crop_id")
    crop_name = request.json.get("crop_name")
    crop_class = request.json.get("crop_class")
    irrigation_per = request.json.get("irrigation_per")
    birth_cycle = request.json.get("birth_cycle")
    yield_per = request.json.get("yield_per")

    res = crop.search_crop(crop_id, crop_name, crop_class, irrigation_per, birth_cycle, yield_per)
    if res is None:
        return jsonify({
            'response': '500',
        })
    resp = {
        'crop_list': [{
            'crop_id': re[0],
            'crop_name': re[1],
            'crop_class': re[2],
            'irrigation_per': re[3],
            'birth_cycle': re[4],
            'yield_per': re[5],
        } for re in res]}
    return jsonify(resp)
