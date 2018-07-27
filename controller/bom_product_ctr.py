# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from flask import Blueprint, jsonify, request, render_template
from manager import bom_product_mgr
from db import constant_params as cp

bom_product_do = Blueprint('bom_product_do', __name__)


@bom_product_do.route('/index')
def index():
    return render_template("bom_product/index.html")


# 获取分页数据
@bom_product_do.route('/get_page', methods=['POST'])
def get_page():
    pageNumber = int(request.form.get('pageNumber', default=cp.default_page_number))
    pageSize = int(request.form.get('pageSize', default=cp.default_page_size))
    if pageNumber <= 0:
        pageNumber = cp.default_page_number
    bom_name = request.form.get('bom_name')
    bom_code = request.form.get('bom_code')
    res = bom_product_mgr.get_page(pageNumber, pageSize, bom_name, bom_code)
    return jsonify(res)


@bom_product_do.route('/pre_add')
def pre_add():
    return render_template("bom_product/pre_add.html")


# 添加
@bom_product_do.route('/add', methods=['POST'])
def add():
    bom_name = request.form.get('bom_name')
    bom_code = request.form.get('bom_code')
    factory_code = request.form.get('factory_code')
    res = bom_product_mgr.add(bom_name, bom_code, factory_code)
    return jsonify(res)


# 删除
@bom_product_do.route('/delete', methods=['POST', 'GET'])
def delete():
    bom_id = None
    if request.method == "GET":
        bom_id = request.args.get('bom_id')
    elif request.method == "POST":
        bom_id = request.form.get('bom_id')
    res = bom_product_mgr.delete(bom_id)
    return jsonify(res)


@bom_product_do.route('/pre_update')
def pre_update():
    bom_id = None
    if request.method == "GET":
        bom_id = request.args.get('bom_id')
    elif request.method == "POST":
        bom_id = request.form.get('bom_id')
    bom_product = bom_product_mgr.get_by_id(bom_id)
    return render_template("bom_product/pre_update.html", bom_product=bom_product)


# 更新
@bom_product_do.route('/update', methods=['POST'])
def update():
    bom_id = request.form.get('bom_id')
    bom_name = request.form.get('bom_name')
    bom_code = request.form.get('bom_code')
    factory_code = request.form.get('factory_code')
    res = bom_product_mgr.update(bom_id, bom_name, bom_code, factory_code)
    return jsonify(res)


# 成本计算
@bom_product_do.route('/calculate_cost', methods=['GET'])
def calculate_cost():
    bom_code = request.form.get('bom_code')
    from manager import result_manager
    result_manager.calculate_all_cost(bom_code=bom_code)
    res = dict()
    res["status"] = 1
    res["msg"] = u"成本计算完成,请刷新重看数据"
    return jsonify(res)


# 树状视图
@bom_product_do.route('/tree_index', methods=['GET', 'POST'])
def tree_index():
    return render_template("bom_product/tree_view.html")


# 树状视图
@bom_product_do.route('/tree_data', methods=['GET', 'POST'])
def tree_data():
    from manager import result_manager
    res = result_manager.get_tree()
    return jsonify(res)


