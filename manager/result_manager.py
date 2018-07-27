# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from db.db_util import get_conn
import sys
from manager import bom_product_mgr
from manager import bom_composite_mgr
from manager import bom_input_mgr
from manager import bom_rel_mgr

table_name = "t_bom_product"


def get_tree(bom_name=None, bom_code=None):
    res = []
    product_s = bom_product_mgr.get_page(1, sys.maxint, bom_name, bom_code).get("data")
    for product in product_s:
        ele = dict()
        ele["pid"] = 0
        ele["id"] = product.get("bom_code")
        ele["name"] = product.get("bom_name")
        ele["factory"] = product.get("factory_code")
        ele["cost"] = product.get("bom_cost")
        res.append(ele)

    composite_s = bom_composite_mgr.get_all_for_tree()
    for composite in composite_s:
        ele = dict()
        ele["pid"] = composite.get("bom_code")
        bom_input = bom_input_mgr.get_by_code(composite.get("com_code"))[0]
        ele["id"] = bom_input.get("bom_code")
        ele["name"] = bom_input.get("bom_name")
        ele["cnt"] = composite.get("com_cnt")
        ele["unit"] = bom_input.get("bom_unit")
        ele["unit_price"] = bom_input.get("bom_unit_price")
        ele["rate"] = bom_input.get("bom_rate")
        ele["is_produce"] = bom_input.get("is_produce")
        res.append(ele)

    rel_s = bom_rel_mgr.get_all_for_tree()
    for rel in rel_s:
        ele = dict()
        ele["pid"] = rel.get("bom_code")
        bom_input = bom_input_mgr.get_by_code(rel.get("com_code"))[0]
        ele["id"] = bom_input.get("bom_code")
        ele["name"] = bom_input.get("bom_name")
        ele["cnt"] = rel.get("com_cnt")
        ele["unit"] = bom_input.get("bom_unit")
        ele["unit_price"] = bom_input.get("bom_unit_price")
        ele["rate"] = bom_input.get("bom_rate")
        ele["is_produce"] = bom_input.get("is_produce")
        res.append(ele)

    print(len(res))
    return res


def calculate_all_cost(bom_name=None, bom_code=None):
    product_s = bom_product_mgr.get_page(1, sys.maxint, bom_name, bom_code).get("data")
    counter = 0
    conn = get_conn()
    cur = conn.cursor()
    for product in product_s:
        bom_code = product.get("bom_code")
        bom_cost = calculate_product_cost(bom_code)
        sql = "update " + table_name + " set bom_cost=%f where bom_code='%s'" \
              % (bom_cost, bom_code)
        cur.execute(sql)
        if counter == 100:
            conn.commit()
            counter = 0
    conn.commit()


def calculate_product_cost(bom_code):
    # 根据商品组成, 找到各个组件
    composite_s = bom_composite_mgr.get_by_bom_code(bom_code)
    res = 0
    for composite in composite_s:
        com_code = composite.get("com_code")
        cnt = composite.get("com_cnt")
        res += calculate_composite_cost(com_code, res=0, cnt=cnt)
    return res


def calculate_composite_cost(com_code, res=0, cnt=1):
    # 找到组件
    composite = bom_input_mgr.get_by_code(com_code)[0]
    # print(composite)
    # 如果组件是外购的, 则直接返回组件单价
    if composite.get("is_produce") == 0:
        res += composite.get("bom_unit_price") * cnt
        # print("添加组件：" + composite.get("bom_name") + ":" + str(cnt) + ":共计："
        # + str(composite.get("bom_unit_price") * cnt))
    # 如果组件是自制的,则递归计算其成本
    else:
        c_c = bom_rel_mgr.get_by_bom_code(com_code)
        for c in c_c:
            com_code = c.get("com_code")
            cnt = c.get("com_cnt", 1)
            res = calculate_composite_cost(com_code, res=res, cnt=cnt)
    return res


if __name__ == '__main__':
    # a = calculate_product_cost("JJCY001")
    # calculate_all_cost()
    # 142.0625
    # a = calculate_composite_cost("YZMP0001")
    # print(a)
    get_tree()
