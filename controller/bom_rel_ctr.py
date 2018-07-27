# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from flask import Blueprint, jsonify, request, render_template
from manager import bom_rel_mgr
from manager import bom_input_mgr
from db import constant_params as cp

bom_rel_do = Blueprint('bom_rel_do', __name__)


# 获取分页数据
@bom_rel_do.route('/get_page', methods=['POST'])
def get_page():
    pageNumber = int(request.form.get('pageNumber', default=cp.default_page_number))
    pageSize = int(request.form.get('pageSize', default=cp.default_page_size))
    if pageNumber <= 0:
        pageNumber = cp.default_page_number
    bom_code = request.form.get('bom_code')
    com_name = request.form.get('com_name')
    com_code = request.form.get('com_code')
    res = bom_rel_mgr.get_page(pageNumber, pageSize, bom_code, com_name, com_code)
    return jsonify(res)


@bom_rel_do.route('/pre_add', methods=['GET'])
def pre_add():
    bom_code = request.args.get('bom_code')
    bom_input = bom_input_mgr.get_by_code(bom_code)[0]
    return render_template("bom_rel/pre_add.html", bom_input=bom_input)


@bom_rel_do.route('/add', methods=['POST'])
def add():
    bom_code = request.form.get('bom_code')
    bom_name = request.form.get('bom_name')
    com_cnt = request.form.get('com_cnt_add_form')
    com_name = request.form.get('com_name_add_form')
    com_code = request.form.get('com_code_add')
    com_unit_price = request.form.get('com_unit_price_add_form')
    com_unit = request.form.get('com_unit_add_form')
    com_rate = request.form.get('com_rate_add')
    res = bom_rel_mgr.add(bom_name=bom_name, bom_code=bom_code,
                          com_code=com_code, com_name=com_name, com_rate=com_rate,
                          com_unit=com_unit, com_unit_price=com_unit_price, com_cnt=com_cnt)
    return jsonify(res)


# 删除
@bom_rel_do.route('/delete', methods=['POST', 'GET'])
def delete():
    rel_id = None
    if request.method == "GET":
        rel_id = request.args.get('rel_id')
    elif request.method == "POST":
        rel_id = request.form.get('rel_id')
    res = bom_rel_mgr.delete_by_id(rel_id)
    return jsonify(res)


@bom_rel_do.route('/pre_update')
def pre_update():
    rel_id = None
    if request.method == "GET":
        rel_id = request.args.get('rel_id')
    elif request.method == "POST":
        rel_id = request.form.get('rel_id')
    bom_rel = bom_rel_mgr.get_by_id(rel_id)
    return render_template("bom_rel/pre_update.html", bom_rel=bom_rel)


@bom_rel_do.route('/update', methods=['POST'])
def update():
    rel_id = request.form.get('rel_id')
    bom_code = request.form.get('bom_code')
    bom_name = request.form.get('bom_name')
    com_cnt = request.form.get('com_cnt_update_form')
    com_name = request.form.get('com_name_update_form')
    com_code = request.form.get('com_code_update')
    com_unit_price = request.form.get('com_unit_price_update_form')
    com_unit = request.form.get('com_unit_update_form')
    com_rate = request.form.get('com_rate_update')
    res = bom_rel_mgr.update(c_id=rel_id, bom_name=bom_name, bom_code=bom_code,
                                   com_code=com_code, com_name=com_name, com_rate=com_rate,
                                   com_unit=com_unit, com_unit_price=com_unit_price, com_cnt=com_cnt)
    return jsonify(res)
