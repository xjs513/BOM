# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from flask import Blueprint, jsonify, request, render_template
from manager import bom_composite_mgr
from db import constant_params as cp

bom_composite_do = Blueprint('bom_composite_do', __name__)


# 获取分页数据
@bom_composite_do.route('/get_page', methods=['POST'])
def get_page():
    pageNumber = int(request.form.get('pageNumber', default=cp.default_page_number))
    pageSize = int(request.form.get('pageSize', default=cp.default_page_size))
    if pageNumber <= 0:
        pageNumber = cp.default_page_number
    bom_code = request.form.get('bom_code')
    com_name = request.form.get('com_name')
    com_code = request.form.get('com_code')
    res = bom_composite_mgr.get_page(pageNumber, pageSize, bom_code, com_name, com_code)
    return jsonify(res)


@bom_composite_do.route('/pre_add', methods=['GET'])
def pre_add():
    bom_code = request.args.get('bom_code')
    from manager import bom_product_mgr
    bom_product = bom_product_mgr.get_by_code(bom_code)
    return render_template("bom_composite/pre_add.html", bom_product=bom_product)


@bom_composite_do.route('/add', methods=['POST'])
def add():
    bom_code = request.form.get('bom_code')
    bom_name = request.form.get('bom_name')
    factory_code = request.form.get('factory_code')
    com_cnt = request.form.get('com_cnt_add_form')
    com_name = request.form.get('com_name_add_form')
    com_code = request.form.get('com_code_add')
    com_unit_price = request.form.get('com_unit_price_add_form')
    com_unit = request.form.get('com_unit_add_form')
    com_rate = request.form.get('com_rate_add')
    res = bom_composite_mgr.add(bom_name=bom_name, bom_code=bom_code, factory_code=factory_code,
                                com_code=com_code, com_name=com_name, com_rate=com_rate,
                                com_unit=com_unit, com_unit_price=com_unit_price, com_cnt=com_cnt)
    return jsonify(res)


# 删除
@bom_composite_do.route('/delete', methods=['POST', 'GET'])
def delete():
    composite_id = None
    if request.method == "GET":
        composite_id = request.args.get('composite_id')
    elif request.method == "POST":
        composite_id = request.form.get('composite_id')
    res = bom_composite_mgr.delete_by_id(composite_id)
    return jsonify(res)


@bom_composite_do.route('/pre_update')
def pre_update():
    composite_id = None
    if request.method == "GET":
        composite_id = request.args.get('composite_id')
    elif request.method == "POST":
        composite_id = request.form.get('composite_id')
    bom_composite = bom_composite_mgr.get_by_id(composite_id)
    return render_template("bom_composite/pre_update.html", bom_composite=bom_composite)


@bom_composite_do.route('/update', methods=['POST'])
def update():
    composite_id = request.form.get('composite_id')
    bom_code = request.form.get('bom_code')
    bom_name = request.form.get('bom_name')
    factory_code = request.form.get('factory_code')
    com_cnt = request.form.get('com_cnt_update_form')
    com_name = request.form.get('com_name_update_form')
    com_code = request.form.get('com_code_update')
    com_unit_price = request.form.get('com_unit_price_update_form')
    com_unit = request.form.get('com_unit_update_form')
    com_rate = request.form.get('com_rate_update')
    res = bom_composite_mgr.update(c_id=composite_id, bom_name=bom_name, bom_code=bom_code, factory_code=factory_code,
                                   com_code=com_code, com_name=com_name, com_rate=com_rate,
                                   com_unit=com_unit, com_unit_price=com_unit_price, com_cnt=com_cnt)
    # def update(c_id, bom_name, bom_code, com_name, com_code, com_cnt,
    # com_unit, com_unit_price, com_rate, factory_code):
    return jsonify(res)

# print(request.form)
# for ele in request.form:
#     print(ele + ":" + request.form.get(ele))
#
# print("********************************")
# com_cnt_add_form:45.00
# com_name_add_form:黑龙东北大米
# com_code_add:ABC0001
# com_unit_price_add_form:2.1
# com_unit_add_form:KG
# factory_code:5400
# com_rate_add:3
# bom_name:营养快线青春版
# bom_code:YL_000112