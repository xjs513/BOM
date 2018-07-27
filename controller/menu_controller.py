# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from flask import Blueprint, jsonify
from manager import menu_manager
menu = Blueprint('menu', __name__)


@menu.route('/get_tree', methods=['POST', 'GET'])
def get_tree():
    res = dict()
    res = menu_manager.get_tree()
    return jsonify(res)
