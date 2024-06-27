from run import app
from flask import request, jsonify
import dbapi as db


@app.route('/sale_list')
def get_sale_list():
    sale_list = db.get_sale_list()
    resp = {
        'sale_list': sale_list
    }
    return jsonify(resp)


@app.route('/new_orders', methods=['POST'])
def new_orders():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    product_quantity = int(request.json.get('product_quantity'))
    if None in (product_id, user_id, product_quantity):
        return jsonify({
            'response': 'None input'
        })

    res = db.new_orders(user_id, product_id, product_quantity)
    db.sub_goods_quantity(product_id, product_quantity)
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


@app.route('/get_orders_list')
def get_orders_list():
    orders_list = db.get_orders_list()
    return jsonify({
        'orders_list': orders_list
    })


@app.route('/get_user_orders_list')
def get_user_orders_list():
    user_id = request.args.get('user_id')
    if user_id is None:
        orders_list = db.get_orders_list()
    else:
        orders_list = db.get_orders_list_user_id(user_id)
    if orders_list is None:
        return jsonify({
            'response': 'database false'
        })
    else:
        return jsonify({
            'orders_list': orders_list
        })


@app.route('/del_orders')
def del_orders():
    orders_id = request.args.get('order_id')
    res = db.del_orders(orders_id)
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
