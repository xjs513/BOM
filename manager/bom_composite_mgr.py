# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from db.db_util import get_conn, is_not_blank, get_result_dict, get_res_dict
import config
table_name = "t_bom_composite"


def get_by_bom_code(bom_code):
    conn = get_conn()
    cur = conn.cursor()
    sql = "select * from " + table_name + " where bom_code='%s'" % (bom_code,)
    cur.execute(sql)
    res = get_result_dict(cur)
    cur.close()
    # conn.close()
    return res


def get_by_id(c_id):
    conn = get_conn()
    cur = conn.cursor()
    sql = "select * from " + table_name + " where id=%d" % (int(c_id),)
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    # conn.close()
    return res


def get_page(page_number, page_size, bom_code=None, com_name=None, com_code=None):
    count_sql = "select count(1) AS num from %s where bom_code='%s' " % (table_name, bom_code)
    if int(page_number) <= 1:
        pager_sql = "select top %d * from %s WHERE bom_code='%s' " % (int(page_size), table_name , bom_code)
    else:
        pager_sql = "select top %d * from %s WHERE bom_code='%s' AND id not in(select top %d id from %s) " %\
          (int(page_size), table_name, bom_code, int(page_number-1) * int(page_size), table_name)
    if is_not_blank(com_name):
        pager_sql += " and com_name like '%%%s%%'" % (com_name,)
        count_sql += " and com_name like '%%%s%%'" % (com_name,)
    if is_not_blank(com_code):
        pager_sql += " and com_code like '%%%s%%'" % (com_code,)
        count_sql += " and com_code like '%%%s%%'" % (com_code,)
    # select top 分页条数 * from 表名 where 主键 not in(select top 20 主键 from 表名)
    res = dict()
    print(count_sql)
    print(pager_sql)
    cur = get_conn().cursor()
    cur.execute(count_sql)
    res["total"] = cur.fetchone()["num"]

    cur.execute(pager_sql)
    data = get_result_dict(cur)
    cur.close()
    res["pageNumber"] = page_number
    res["pageSize"] = page_size
    res["data"] = data
    return res


def get_all_for_tree():
    sql = "select * from %s " % (table_name, )
    res = dict()
    cur = get_conn().cursor()
    cur.execute(sql)
    data = get_result_dict(cur)
    cur.close()
    return data


# 向数据库中添加数据
def add(bom_name, bom_code, com_name, com_code, com_cnt, com_unit, com_unit_price, com_rate, factory_code):
    print(com_unit_price)
    print(com_cnt)
    conn = get_conn()
    cur = conn.cursor()
    res = dict()
    if check_add_exist(cur, bom_code, com_code):
        res["status"] = 0
        res["msg"] = u"组件已在该物料组成中"
    else:
        sql = "insert into " + table_name \
              + "(bom_name, bom_code, com_name, com_code, com_cnt, com_unit, " \
            "com_unit_price, com_rate, factory_code) " \
            "VALUES ('%s','%s','%s','%s',%f,'%s',%f,%d,%d)" % \
              (bom_name, bom_code, com_name, com_code, float(com_cnt), com_unit,
               float(com_unit_price), int(com_rate), int(factory_code))
        cur.execute(sql)
        conn.commit()
        total = cur.rowcount
        # cur.close()
        # conn.close()
        res = get_res_dict(total)
    return res


def check_add_exist(cur, bom_code, com_code):
    sql = "select count(1) AS num from %s WHERE bom_code='%s' AND com_code='%s' " % (table_name, bom_code, com_code)
    try:
        cur.execute(sql)
        return cur.fetchone()["num"] > 0
    except Exception as err:
        print(str(err))


def check_update_exist(cur, c_id, bom_code, com_code):
    sql = "select count(1) AS num from %s WHERE bom_code='%s' AND com_code='%s' AND id <>%d" % \
          (table_name, bom_code, com_code, int(c_id))
    try:
        print(sql)
        cur.execute(sql)
        return cur.fetchone()["num"] > 0
    except Exception as err:
        print(str(err))


# 删除数据
def delete_by_id(c_id):
    res = dict()
    conn = get_conn()
    cur = conn.cursor()
    sql = "delete from  " + table_name + " where id=%d" % (int(c_id),)
    print(sql)
    cur.execute(sql)
    conn.commit()
    total = cur.rowcount
    res = get_res_dict(total)
    return res


# 删除数据
def delete_by_bom_code(bom_code):
    res = dict()
    conn = get_conn()
    cur = conn.cursor()
    sql = "delete from  " + table_name + " where bom_code='%s'" % (bom_code,)
    print(sql)
    cur.execute(sql)
    conn.commit()
    total = cur.rowcount
    res = get_res_dict(total)
    return res


def update(c_id, bom_name, bom_code, com_name, com_code, com_cnt, com_unit, com_unit_price, com_rate, factory_code):
    conn = get_conn()
    cur = conn.cursor()
    res = dict()
    # def check_update_exist(cur, c_id, bom_code, com_code):
    if check_update_exist(cur, c_id, bom_code, com_code):
        res["status"] = 0
        res["msg"] = u"组件已在该物料组成中"
    else:
        sql = "update " + table_name + " set bom_name='%s', bom_code='%s',com_name='%s', com_code='%s'," \
               "com_cnt=%f, com_unit='%s', com_unit_price=%f, com_rate=%d,factory_code=%d where id=%d" \
              % (bom_name, bom_code, com_name, com_code, float(com_cnt),
                 com_unit, float(com_unit_price), int(com_rate), int(factory_code), int(c_id))
        print(sql)
        cur.execute(sql)
        conn.commit()
        total = cur.rowcount
        cur.close()
        # conn.close()
        res = get_res_dict(total)
    return res
