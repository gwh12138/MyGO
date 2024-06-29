import flask
from flask import Flask, render_template, request, redirect, url_for
from app import app
from api_field import *
from backend.login import *
from api_product import *
from api_product_storage import *
from api_goods import *
from api_sale import *


@app.route("/")
def index():
    return flask.render_template('./login.html')


@app.route("/index.html")
def index_html():
    user_name = request.args.get('user_name')
    return flask.render_template('./index.html', user_name=user_name)


@app.route("/user_info.html")
def user_info_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./user_info.html', user_id=user_id)


@app.route("/customer.html")
def customer_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./customer.html', user_id=user_id)


@app.route("/customer_buy.html")
def customer_buy_html():
    user_id = request.args.get('user_id')
    product_id = request.args.get('product_id')
    return flask.render_template('./customer_buy.html', user_id=user_id, product_id=product_id)


@app.route("/field_add.html")
def field_add_html():
    return flask.render_template('./field_add.html')


@app.route("/field_change.html")
def field_change_html():
    field_id = request.args.get('field_id')
    return flask.render_template('./field_change.html', field_id=field_id)


@app.route("/product_add.html")
def product_add_html():
    return flask.render_template('./product_add.html')


@app.route("/field.html")
def field_html():
    return flask.render_template('./field.html')


@app.route("/storage.html")
def storage_html():
    return flask.render_template('./storage.html')


@app.route("/goods.html")
def goods_html():
    return flask.render_template('./goods.html')


@app.route("/product.html")
def product_html():
    return flask.render_template('./product.html')


@app.route("/product_change.html")
def product_change_html():
    product_id = request.args.get('product_id')
    return flask.render_template('./product_change.html', product_id=product_id)


@app.route("/storage_add.html")
def storage_add_html():
    return flask.render_template('./storage_add.html')


@app.route("/storage_change.html")
def storage_change_html():
    product_id = request.args.get('product_id')
    field_id = request.args.get('field_id')
    return flask.render_template('./storage_change.html', product_id=product_id, field_id=field_id)


@app.route("/goods_add.html")
def goods_add_html():
    return flask.render_template('./goods_add.html')


@app.route("/goods_change.html")
def goods_change_html():
    product_id = request.args.get('product_id')
    return flask.render_template('./goods_change.html', product_id=product_id)


@app.route("/order.html")
def order_html():
    return flask.render_template('./order.html')


@app.route("/order_change.html")
def order_change_html():
    order_id = request.args.get('order_id')
    return flask.render_template('./order_change.html', order_id=order_id)


@app.route('/welcome.html')
def welcome_html():
    return flask.render_template('./welcome.html')


@app.route("/account.html")
def account_html():
    return flask.render_template('./account.html')


@app.route("/index_customer.html")
def index_customer_html():
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return flask.render_template('./index_customer.html', user_id=user_id, user_name=user_name)


@app.route("/customer_order.html")
def customer_order_html():
    user_id = request.args.get('user_id')
    return flask.render_template('./customer_order.html', user_id=user_id)


@app.route("/index_worker.html")
def index_worker_html():
    user_name = request.args.get('user_name')
    return flask.render_template('./index_worker.html', user_name=user_name)


@app.route("/index_admin.html")
def index_admin_html():
    user_name = request.args.get('user_name')
    return flask.render_template('./index_admin.html', user_name=user_name)


@app.route('/01.jpg')
def img01():
    return app.send_static_file('01.jpg')


if __name__ == '__main__':
    app.run(debug=True)
