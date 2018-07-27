# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from flask import Blueprint, jsonify, request, render_template
from manager import bom_input_mgr
from db import constant_params as cp

bom_input_do = Blueprint('bom_input_do', __name__)


@bom_input_do.route('/index')
def index():
    return render_template("bom_input/index.html")


# 获取分页数据
@bom_input_do.route('/get_page', methods=['POST'])
def get_page():
    pageNumber = int(request.form.get('pageNumber', default=cp.default_page_number))
    pageSize = int(request.form.get('pageSize', default=cp.default_page_size))
    if pageNumber <= 0:
        pageNumber = cp.default_page_number
    bom_name = request.form.get('bom_name')
    bom_code = request.form.get('bom_code')
    res = bom_input_mgr.get_page(pageNumber, pageSize, bom_name, bom_code)
    return jsonify(res)


@bom_input_do.route('/get_rate_s', methods=['POST'])
def get_rate_s():
    res = bom_input_mgr.get_rate_s()
    return jsonify(res)


@bom_input_do.route('/get_by_rate', methods=['POST'])
def get_by_rate():
    bom_rate = request.form.get('bom_rate')
    print(bom_rate)
    res = bom_input_mgr.get_by_rate(bom_rate)
    return jsonify(res)


@bom_input_do.route('/get_by_code', methods=['POST'])
def get_by_code():
    bom_code = request.form.get('bom_code')
    print(bom_code)
    res = bom_input_mgr.get_by_code(bom_code)
    return jsonify(res)


@bom_input_do.route('/pre_add')
def pre_add():
    return render_template("bom_input/pre_add.html", bom_rate_dict=cp.bom_rate_dict,
                           bom_unit_list=cp.bom_unit_list)


# 添加
@bom_input_do.route('/add', methods=['POST'])
def add():
    bom_name = request.form.get('bom_name')
    bom_code = request.form.get('bom_code')
    bom_rate = request.form.get('bom_rate')
    bom_unit = request.form.get('bom_unit')
    bom_unit_price = request.form.get('bom_unit_price')
    is_produce = request.form.get('is_produce')
    res = bom_input_mgr.add(bom_name, bom_code, bom_rate, bom_unit, bom_unit_price, is_produce)
    return jsonify(res)


# 删除
@bom_input_do.route('/delete', methods=['POST', 'GET'])
def delete():
    bom_id = None
    if request.method == "GET":
        bom_id = request.args.get('bom_id')
    elif request.method == "POST":
        bom_id = request.form.get('bom_id')
    res = bom_input_mgr.delete(bom_id)
    return jsonify(res)


@bom_input_do.route('/pre_update')
def pre_update():
    bom_id = None
    if request.method == "GET":
        bom_id = request.args.get('bom_id')
    elif request.method == "POST":
        bom_id = request.form.get('bom_id')
    base_bom = bom_input_mgr.get_by_id(bom_id)
    return render_template("bom_input/pre_update.html",bom_rate_dict=cp.bom_rate_dict,
                           bom_unit_list=cp.bom_unit_list,base_bom=base_bom)


# 更新
@bom_input_do.route('/update', methods=['POST'])
def update():
    bom_id = request.form.get('bom_id')
    bom_name = request.form.get('bom_name')
    bom_code = request.form.get('bom_code')
    bom_rate = request.form.get('bom_rate')
    bom_unit = request.form.get('bom_unit')
    bom_unit_price = request.form.get('bom_unit_price')
    is_produce = request.form.get('is_produce')
    res = bom_input_mgr.update(bom_id, bom_name, bom_code, bom_rate, bom_unit, bom_unit_price, is_produce)
    return jsonify(res)
