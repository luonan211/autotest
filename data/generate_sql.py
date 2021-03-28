# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 15:34
# AUTHOR   : luo nan
# FILE     : generate_sql.py
# SOFTWARE : PyCharm
# FUNCTION :

import datetime
import pymysql
from toolkit.time_measure import time_measure


class GenerateInsertSql:
    def __init__(self, sql, table, host='localhost', port=3306, user='root', passwd='mima123456', db='bobmydata'):
        self.sql = sql
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.db = db
        self.table = table

    @time_measure
    def conn_mysql(self):
        """

        :return:
        """
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset='utf8mb4'
            # use_unicode=True
          )

        cursor = conn.cursor()
        cursor.execute(self.sql)
        rows = cursor.fetchall()
        filed = cursor.description

        return filed, rows

    @time_measure
    def generate_insert_into_sql(self):
        """

        :return:
        """
        fileds, data = self.conn_mysql()

        insert_data = []
        filed_list = []

        # 获取插入的字段
        for f in fileds:
            filed_list.append(f[0])

        # 转换为元组->str并去掉引号
        filed_tuple = tuple(filed_list)
        # print(filed_tuple)
        print("带插入数据的长度为{}".format(len(filed_tuple)))
        str_filed = str(filed_tuple).replace("\'", "")

        # 数据处理, 处理datetime.datetime类型的数据。转化为 YYYY-mm-dd HH:MM:SS
        new_data = []
        for row in data:
            new_row = []
            for e in row:
                if isinstance(e, datetime.datetime):
                    e = datetime.datetime.strftime(e, "%Y-%m-%d %H:%M:%S")
                    new_row.append(e)
                elif e is None:
                    e = ''
                    new_row.append(e)
                else:
                    new_row.append(e)

            # print("处理后的数据长度：{}".format(len(new_row)))
            new_data.append(tuple(new_row))

        # 拼装sql
        # print(new_data)
        for row in new_data:
            sql = "INSERT INTO {}.{} {}VALUES {};".format(self.db.upper(), self.table.upper(), str_filed, row)
            insert_data.append(sql)

        return insert_data

    @time_measure
    def generate_sql_txt(self):
        """

        :return:
        """
        filename = self.table + ".txt"
        data = self.generate_insert_into_sql()
        print(len(data))
        with open(filename, mode='w', buffering=True) as f:
            for row in data:
                f.write(row+"\n")

        print("数据已生成，请检查当前目录下的{}".format(filename))


if __name__ == '__main__':
    sql = "select * from product_product;"
    table_name = "product_product"
    p = GenerateInsertSql(sql=sql, table=table_name)

    p.generate_sql_txt()