# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from db.db_util import get_conn, is_not_blank, get_result_dict, check_add_exist, get_res_dict, check_update_exist

table_name = "t_bom_product"


def get_by_id(bom_id):
    conn = get_conn()
    cur = conn.cursor()
    sql = "select * from " + table_name + " where bom_id=%d" % (int(bom_id),)
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    # conn.close()
    return res


def get_by_code(bom_code):
    conn = get_conn()
    cur = conn.cursor()
    sql = "select * from " + table_name + " where bom_code='%s'" % (bom_code,)
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    # conn.close()
    return res


def get_page(page_number, page_size, bom_name=None, bom_code=None):
    count_sql = "select count(1) AS num from %s where 1>0 " % (table_name, )
    if int(page_number) <= 1:
        pager_sql = "select top %d * from %s WHERE bom_id>0 " % (int(page_size), table_name)
    else:
        pager_sql = "select top %d * from %s WHERE bom_id not in(select top %d bom_id from %s) " %\
          (int(page_size), table_name, int(page_number-1) * int(page_size), table_name)
    if is_not_blank(bom_name):
        pager_sql += " and bom_name like '%%%s%%'" % (bom_name,)
        count_sql += " and bom_name like '%%%s%%'" % (bom_name,)
    if is_not_blank(bom_code):
        pager_sql += " and bom_code like '%%%s%%'" % (bom_code,)
        count_sql += " and bom_code like '%%%s%%'" % (bom_code,)
    # select top 分页条数 * from 表名 where 主键 not in(select top 20 主键 from 表名)
    res = dict()
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


# 向数据库中添加数据
def add(bom_name, bom_code, factory_code):
    conn = get_conn()
    cur = conn.cursor()
    res = dict()
    if check_add_exist(cur, table_name, "bom_name", bom_name):
        res["status"] = 0
        res["msg"] = u"物料名称已存在"
    elif check_add_exist(cur, table_name, "bom_code", bom_code):
        res["status"] = 0
        res["msg"] = u"物料编码已存在"
    else:
        sql = "insert into " + table_name + "(bom_name, bom_code, factory_code) " \
            "VALUES ('%s','%s',%d)" % (bom_name, bom_code, int(factory_code))
        cur.execute(sql)
        conn.commit()
        total = cur.rowcount
        # cur.close()
        # conn.close()
        res = get_res_dict(total)
    return res


# 删除数据
def delete(bom_id):
    res = dict()
    conn = get_conn()
    cur = conn.cursor()
    sql = "delete from  " + table_name + " where bom_id=%d" % (int(bom_id),)
    print(sql)
    cur.execute(sql)
    conn.commit()
    total = cur.rowcount
    res = get_res_dict(total)
    return res


def update(bom_id, bom_name, bom_code, factory_code):
    conn = get_conn()
    cur = conn.cursor()
    res = dict()
    if check_update_exist(cur, table_name, "bom_name", bom_name, "bom_id", int(bom_id)):
        res["status"] = 0
        res["msg"] = u"物料名称已存在"
    elif check_update_exist(cur, table_name, "bom_code", bom_code, "bom_id", int(bom_id)):
        res["status"] = 0
        res["msg"] = u"物料编码已存在"
    else:
        sql = "update " + table_name + " set bom_name='%s', bom_code='%s', factory_code=%d " \
               "where bom_id=%d" \
              % (bom_name, bom_code, int(factory_code), int(bom_id))
        cur.execute(sql)
        conn.commit()
        total = cur.rowcount
        cur.close()
        # conn.close()
        res = get_res_dict(total)
    return res
