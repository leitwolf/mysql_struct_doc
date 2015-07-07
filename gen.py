#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: lonewolf
# Date: 2015-04-09 20:21:57
#

#
# 生成mysql表结构到html
#

import os.path
import optparse
import pymysql
import sys


# 版本2
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')


# 表模板
TABLE_TEMPLATE = """
<p>-----------------------------</p>
<span>表名称: {{table_name}}</span></br>
<span>注释: {{table_comment}}</span>
<table cellspacing='0'>
<thead><tr><th>列</th><td>类型</td><td>注释</td></tr></thead>
{{items}}
</table>
</br>
"""


# 表项目模板
TABLE_ITEM_TEMPLATE = """<tr><th>{{column_name}}<td>{{data_type}}</td><td>{{comment}}</td></th></tr>
"""


# 读取文件
def read_file(path):
    f = open(path, "r")
    content = f.read()
    f.close()
    return content


# 写入文件
def write_file(path, content):
    f = open(path, "w+")
    f.write(content)
    f.close()


#
# 处理数据，输出string
# @param host string 域名
# @param port string 端口
# @param user string 用户名
# @param password string 密码
# @param db string 数据库名称
# @return string 返回生成的html
#
def get_data(host, port, user, password, db):
    try:
        conn = pymysql.connect(
            host=host, port=port, user=user, passwd=password, db=db, charset='utf8')
    except Exception as e:
        print("Error:"+str(e))
        print("")
        return None

    # 游标
    cursor = conn.cursor()

    # 总字符
    all_str = ""

    # 查询表列表
    cursor.execute("select TABLE_NAME,TABLE_COMMENT from information_schema.tables where table_schema='" +
                   db + "' and table_type='base table'")
    table_names = []
    table_comments = []
    for row in cursor:
        table_names.append(row[0])
        table_comments.append(row[1])

    length = len(table_names)
    for i in range(1, length):
        table_name = table_names[i]
        # 查询表结构
        print("Export table: "+table_name)
        cursor.execute("select COLUMN_NAME,COLUMN_TYPE,COLUMN_COMMENT from information_schema.columns where table_schema='" +
                       db + "' and table_name='" + table_name + "'")
        # 各列字符
        items_str = ""
        for t in cursor:
            column_name = t[0]
            column_type = t[1]
            comment = t[2]

            ts = TABLE_ITEM_TEMPLATE.replace("{{column_name}}", column_name)
            ts = ts.replace("{{data_type}}", column_type)
            ts = ts.replace("{{comment}}", comment)
            items_str += ts

        # 表信息
        table_str = TABLE_TEMPLATE.replace("{{table_name}}", table_name)
        table_str = table_str.replace("{{table_comment}}", table_comments[i])
        table_str = table_str.replace("{{items}}", items_str)

        # 表信息加入到总字符串
        all_str += table_str

    # 关闭数据连接
    cursor.close()
    conn.close()

    return all_str


#
# 生成html
# @param tables_str string 已获取的表结构信息
# @param output_dir string 输出路径
# @return
#
def gen_html(tables_str, output_dir, db):
    # 载入模板
    template = read_file("template.html")
    strs = template.replace("{{db_name}}", db)
    strs = strs.replace("{{content}}", tables_str)
    output_path = os.path.join(output_dir, db+".html")
    write_file(output_path, strs)


# 运行
# @return
#
def run():
    parser = optparse.OptionParser()
    parser.add_option(
        "", "--host", dest="host", help="host, default:localhost")
    parser.add_option("", "--port", dest="port", help="port, default:3306")
    parser.add_option("", "--user", dest="user", help="username, default:root")
    parser.add_option(
        "", "--password", dest="password", help="password, default(empty):")
    parser.add_option("", "--db", dest="db", help="database name")
    parser.add_option("", "--output", dest="output", help="output dir")
    (options, args) = parser.parse_args()
    host = options.host
    port = options.port
    user = options.user
    password = options.password
    db = options.db
    output = options.output
    if host is None:
        host = "localhost"
    if port is None:
        port = 3306
    if user is None:
        user = "root"
    if password is None:
        password = ""
    if db is None:
        print("Error: Please enter db.")
        print("")
        parser.print_help()
        return
    if output is None:
        print("Error: Please enter output.")
        print("")
        parser.print_help()
        return
    if not os.path.exists(output):
        print("Error: path("+output+") not exists")
        print("")
        parser.print_help()
        return

    tables_str = get_data(host, port, user, password, db)
    gen_html(tables_str, output, db)


if __name__ == '__main__':
    run()
