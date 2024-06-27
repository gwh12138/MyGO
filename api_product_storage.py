from run import app
from flask import request, jsonify
import dbapi as db


@app.route('/product_storage_list')
def get_product_storage_list():
    product_id = request.args.get("product_id")
    field_id = request.args.get("field_id")
    if product_id is None and field_id is None:
        product_storage_list = db.get_product_storage_list()
        product_id = 0
        field_id = 0
    elif field_id is None:
        field_id = 0
        product_storage_list = db.get_product_storage_product_id(product_id)
    else:
        product_storage_list = db.get_product_storage(product_id, field_id)
    resp = {
        "product_id": product_id,
        "field_id": field_id,
        "product_storage_list": product_storage_list,
    }

    return jsonify(resp)


@app.route('/change_product_storage', methods=['POST'])
def change_product_storage():
    product_id = request.json.get('product_id')
    field_id = request.json.get('field_id')
    product_quantity = request.json.get('product_quantity')
    product_state = request.json.get('product_state')

    if None in (product_id, field_id, product_quantity, product_state):
        return jsonify({
            'response': 'None input'
        })

    res = db.change_product_storage(product_id, field_id, product_quantity, product_state)
    if res is None:
        return jsonify({
            'response': 'database change field false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'change field false'
        })


@app.route('/add_product_storage', methods=['POST'])
def add_product_storage():
    tt = request
    product_id = request.form.get('product_id')
    field_id = request.form.get('field_id')
    product_quantity = request.form.get('product_quantity')
    product_state = request.form.get('product_state')
    if None in (product_id, field_id, product_quantity, product_state):
        return jsonify({
            'response': 'None input'
        })

    res = db.add_product_storage(product_id, field_id, product_quantity, product_state)
    if res is None:
        return jsonify({
            'response': 'database change field false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'false'
        })


@app.route('/del_product_storage')
def del_product_storage():
    product_id = request.args.get('product_id')
    field_id = request.args.get('field_id')
    if None in (product_id, field_id):
        return jsonify({
            'response': 'None input'
        })

    res = db.del_product_storage(product_id, field_id)
    if res is None:
        return jsonify({
            'response': 'database change field false'
        })
    elif res:
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'change field false'
        })


@app.route('/harvest_product', methods=['POST'])
def harvest_product():
    product_id = request.json.get('product_id')
    field_id = request.json.get('field_id')

    if None in (product_id, field_id):
        return jsonify({
            'response': 'None input'
        })

    res = db.get_product_storage(product_id, field_id)[0]
    product_quantity = int(res['product_quantity'])
    product_state = res['product_state']
    if product_state != 'mature':
        return jsonify({
            'response': 'not mature'
        })

    if db.harvest_product(product_id, product_quantity):
        db.del_product_storage(product_id, field_id)
        return jsonify({
            'response': 'success'
        })
    else:
        return jsonify({
            'response': 'false'
        })




