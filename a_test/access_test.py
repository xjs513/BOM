# encoding=utf-8
# author: kasa
# date: 2018-07-19
# summary: 打印指定access文件、指定表的所有字段

import win32com.client

import pypyodbc


def PrintColumns_pypyodbc(pathfile, tablename):
    connStr = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=%s;' % pathfile
    print('connStr:' + connStr)
    pypyodbc.lowercase = False  # 是否将字段名转为小写
    conn = pypyodbc.connect(connStr)

    headers = []
    result_list = list()
    result_dict = dict()
    cur = conn.cursor()
    cur.execute('SELECT TOP 1 * FROM ' + tablename + " where bom_name like 'ABC%%'")
    for tup in cur.description:
        headers.append(tup[0])
    print headers
    for row in cur.fetchall():
        for field in row:
            print field,
        print ''

        for i in xrange(0, len(row)):
            result_dict[headers[i]] = row[i]
        result_list.append(result_dict)

    print(result_list)

    cur.close()
    conn.close()


PrintColumns_pypyodbc('C:\\code\\bom.accdb', "t_base_bom")
