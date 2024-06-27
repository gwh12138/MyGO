from run import app
from flask import request, jsonify
import dbapi as db


@app.route('/goods_list')
def get_goods_list():
    product_id = request.args.get("product_id")
    if product_id is None:
        product_id = 0
        goods_list = db.get_goods_list()
    else:
        goods_list = db.get_goods_list_id(product_id)
    resp = {
        "product_id": product_id,
        "goods_list": goods_list,
    }
    return resp


@app.route('/change_goods', methods=['POST'])
def change_goods():
    product_id = request.json.get('product_id')
    goods_quantity = request.json.get('goods_quantity')
    goods_price = request.json.get('goods_price')
    goods_state = request.json.get('goods_state')
    if None in (product_id, goods_quantity, goods_price, goods_state):
        return jsonify({
            'response': 'None input'
        })

    res = db.change_goods(product_id, goods_quantity, goods_price, goods_state)
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


@app.route('/add_goods', methods=['POST'])
def add_goods():
    product_id = request.form.get('product_id')
    product_quantity = request.form.get('product_quantity')
    goods_price = request.form.get('goods_price')
    goods_state = request.form.get('goods_state')
    if None in (product_quantity, goods_price, goods_state):
        return jsonify({
            'response': 'None input'
        })

    res = db.add_goods(product_id, product_quantity, goods_price, goods_state)
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


@app.route('/del_goods')
def del_goods():
    product_id = request.args.get('product_id')
    if product_id is None:
        return jsonify({
            'response': 'None input'
        })

    res = db.del_goods(product_id)
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
