# -*- coding: UTF-8 -*-
# !/usr/bin/env python

from db import db_util


def get_tree():
    # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
    conn = db_util.get_conn()
    cur = conn.cursor()
    sql = "select * from t_menu WHERE pid=%d AND display=1 ORDER BY disorder" % (0, )
    cur.execute(sql)
    result_list = db_util.get_result_dict(cur)
    for result_dict in result_list:
        sql = "select * from t_menu WHERE pid=%d AND display=1 ORDER BY disorder" % (result_dict['id'],)
        cur.execute(sql)
        r_2 = db_util.get_result_dict(cur)
        result_dict['children'] = r_2
    # cur.close()
    # conn.close()
    return result_list

