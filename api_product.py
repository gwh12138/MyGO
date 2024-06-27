from app import app
from flask import request, jsonify
import dbapi as db


@app.route('/product_list')
def get_product_list():
    product_class = request.args.get('product_class')
    product_id = request.args.get('product_id')
    if product_class is None and product_id is None:
        product_list = db.get_product_list()
        product_class = 'all'
        product_id = 0
    elif product_class is not None:
        product_id = 0
        product_list = db.get_product_class(product_class)
    else:
        product_class = 'all'
        product_list = db.get_product_by_id(product_id)
    resp = {
        "product_class": product_class,
        "product_id": product_id,
        "product_list": product_list,
    }

    return jsonify(resp)


@app.route('/change_product', methods=['POST'])
def change_product():
    product_id = request.json.get('product_id')
    product_name = request.json.get('product_name')
    product_class = request.json.get('product_class')
    product_price = request.json.get('product_price')

    if None in (product_id, product_name, product_class, product_price):
        return jsonify({
            'response': 'None input'
        })

    res = db.change_product(product_id, product_name, product_class, int(product_price))
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


@app.route('/add_product', methods=['POST'])
def add_product():
    ff = request
    product_name = request.form.get('product_name')
    product_class = request.form.get('product_class')
    product_price = request.form.get('product_price')
    if None in (product_name, product_class, product_price):
        return jsonify({
            'response': 'None input'
        })

    res = db.add_product(product_name, product_class, int(product_price))
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


@app.route('/del_product')
def del_product():
    product_id = request.args.get('product_id')
    if product_id is None:
        return jsonify({
            'response': 'None input'
        })

    res = db.del_product(product_id)
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
