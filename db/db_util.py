#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pypyodbc
import config

reload(sys)
# gbk也可以换成utf—8，如果出现编码问题，这两个都可以试试
# sys.setdefaultencoding('gbk')

conn = None


def get_conn():
    global conn
    if conn is None or conn.connected:
        # filepath是变量，access文件的绝对路径。注意：*.accdb一定要加上
        conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + config.DB_FILE_PATH)
    return conn


def get_result_dict(cur):
    headers = []
    result_list = list()

    for tup in cur.description:
        headers.append(tup[0])
    for row in cur.fetchall():
        result_dict = dict()
        for i in xrange(0, len(row)):
            result_dict[headers[i]] = row[i]
        if "name" in result_dict:
            result_dict["text"] = result_dict.get("name")
        result_list.append(result_dict)
    return result_list


def check_add_exist(cur, table_name, col_name, col_value):
    if type(col_value) == "int":
        sql = "select count(1) AS num from %s WHERE %s=%d" % (table_name, col_name, col_value)
    else:
        sql = "select count(1) AS num from %s WHERE %s='%s'" % (table_name, col_name, col_value)
    try:
        cur.execute(sql)
        return cur.fetchone()["num"] > 0
    except Exception as err:
        print(str(err))
        # config.console_logger.error(str(err) + ":" + sql)
        # config.file_error_logger.error(str(err) + ":" + sql)


def check_update_exist(cur, table_name, col_name, col_value, id_name, id_value):
    if type(col_value) == "int":
        sql = "select count(1) AS num from %s WHERE %s=%d AND %s <>%d" % \
              (table_name, col_name, col_value, id_name, id_value)
    else:
        sql = "select count(1) AS num from %s WHERE %s='%s' AND %s <>%d" % \
              (table_name, col_name, col_value, id_name, id_value)
    try:
        print(sql)
        cur.execute(sql)
        return cur.fetchone()["num"] > 0
    except Exception as err:
        print(str(err))
        # config.console_logger.error(str(err) + ":" + sql)
        # config.file_error_logger.error(str(err) + ":" + sql)


def get_page(sql, page_number, page_size):
    res = dict()
    cur = get_conn().cursor()
    print(sql)
    cur.execute(sql)
    res["total"] = cur.rowcount
    # select top 分页条数 * from 表名 where 主键 not in(select top 20 主键 from 表名)
    sql = sql + " limit %d,%d" % ((page_number - 1) * page_size, page_size)
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    res["pageNumber"] = page_number
    res["pageSize"] = page_size
    res["data"] = data
    return res


def is_blank(ddd):
    if ddd is None:
        return True
    else:
        aaa = str(ddd)
        if aaa.strip() == "":
            return True
        else:
            return False


def is_not_blank(ddd):
    return not is_blank(ddd)


def get_res_dict(total):
    res = dict()
    if total > 0:
        res["status"] = 1
        res["msg"] = u"操作成功"
    else:
        res["status"] = 0
        res["msg"] = u"操作失败"
    return res


# def select_list(sql):
#     conn_in = get_conn()
#     cur = conn.cursor()
#     cur.execute(sql)
#     cnt = 0
#     for tup in cur.description:
#         print(tup[0])
#         cnt += 1
#     print('cnt:' + str(cnt))
#
#     cur.close()
#     conn.close()
#     res = cur.fetchall()
#     return res


def update(sql):
    pass


def insert(sql):
    pass


def delete(sql):
    pass
