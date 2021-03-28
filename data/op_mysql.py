# -*- coding: utf-8 -*- 
# TIME     : 2020/11/30 22:00
# AUTHOR   : luo nan
# FILE     : op_mysql.py
# SOFTWARE : PyCharm
# FUNCTION :

import os
import logging
import queue
import gevent
import pymysql
from dbutils.pooled_db import PooledDB
from urllib.parse import urlparse
from basepath import get_base_path

logger = logging.getLogger(__name__)
DB_POOL = None
query_queue = queue.Queue()
QUEUE_SIZE = 3
db_name = ''
db_host = ''
db_port = ''
db = ''

CONFIG_PATH = os.path.join(get_base_path(), "config", "api-env.properties")


def get_properties_db_config(properties=CONFIG_PATH):
    """从java应用类型的配置文件中读取mysql配置"""
    config_db = {}
    with open(properties, 'r', encoding="utf-8")as f:
        content = f.readlines()

        for line in content:
            if line.find("=") > 0:
                # print(line)
                line = line.replace('\n', '').replace(' ', '')

                k, v = line.split("=")
                # print(type(k))
                # print(k.find('DB'))

                if k.find('DB') > 0:
                    # print(k)
                    config_db[k] = v
    return config_db


def get_mysql_config(db_config):
    """通过解析url，获取连接数据库的要素"""
    mysql_config = {}
    db_url = db_config.get("API_DB_MYSQL_URL")
    url = ":".join(db_url.split(':')[1:])
    # print("预期结果是：mysql://127.0.0.1:3306/bobmydata ==%s" %url)
    parse_url = urlparse(url)

    mysql_config["host"] = parse_url.hostname
    mysql_config["port"] = parse_url.port
    mysql_config["database"] = parse_url.path[1:]
    mysql_config["user"] = db_config.get('API_DB_MYSQL_USER')
    mysql_config["password"] = db_config.get('API_DB_MYSQL_PWD')

    if isinstance(mysql_config["password"],str):
        # print("密码加密")
        new_pwd = ''.join([str(ord(a)) + '*' for a in mysql_config["password"]])
        print("这是新密码:{}".format(new_pwd))
    # print(mysql_config)
    return mysql_config


def get_mysql_connection():
    """

    :return:
    """
    config_db = get_properties_db_config()

    global DB_POOL, db_name, db_host, db_port
    logger.debug(f"链接数据库日志")
    logger.debug(f"数据库配置信息：{config_db}")
    if DB_POOL is None:
        mysql_conf = get_mysql_config(config_db)
        logger.info(f"数据库的配置是：{mysql_conf}")
        print(f"数据库的配置是：{mysql_conf}")
        DB_POOL = PooledDB(pymysql, 10,
                           host=mysql_conf['host'],
                           port=mysql_conf['port'],
                           user=mysql_conf['user'],
                           passwd=mysql_conf['password'],
                           db=mysql_conf['database'],
                           charset='utf8mb4')
        db_name = mysql_conf['password']
        db_host = mysql_conf['host']
        db_port = mysql_conf['port']
        logger.info(f"connect to DB name={db_name}, host={db_host}, port={db_port}")
    logger.info(f"Already connected to DB name={db_name}, host={db_host}, port={db_port}")
    return DB_POOL.connection()


def put_query_in_queue(sql, param):
    """
    :param sql: [str]
    :param param: [tuple]
    :return:
    """
    query_queue.put((sql, param))
    if query_queue.qsize() >= QUEUE_SIZE:
        jobs = [gevent.spawn(execute_queries, query_queue)]
        gevent.joinall(jobs, timeout=60)


def execute_queries(queries):
    """

    :param queries: ()
    :return:
    """
    try:
        connect = get_mysql_connection()
        cursor = connect.cursor()
        size = queries.qsize()
        for i in range(size):
            (query, param) = queries.get()
            logger.info(f"excuting sql {query} with param {param}")
            if param is None:
                cursor.execute(query)
            else:
                cursor.execute(query, param)
            connect.commit()
            queries.task_done()
        # logger.info(f"成功执行{size}条数据修改。")
        logger.info(f"成功执行{size}条数据修改。")
        cursor.close()
        connect.close()
    except Exception:
        logger.exception("捕获一个错误在执行sql中")
        connect.rollback()
        cursor.close()
        connect.close()


def execute_query(sql, param=None):
    """

    :param sql:
    :param param:
    :return:
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        if param is None:
            row_count = cursor.execute(sql)
        else:
            row_count = cursor.execute(sql, param)

        rows = None
        if row_count > 0:
            rows = cursor.fetchall()
            fields = cursor.description
        conn.commit()
        logger.info(f"successfully run query {sql} with param {param}, row_count is {row_count} ")
        cursor.close()
        conn.close()
        return rows, fields
    except Exception:
        logging.exception(f"caught an exceptin during execute query {sql} with {param}")
        conn.rollback()
        cursor.close()
        conn.close()
        return None


if __name__ == '__main__':
    data, field = execute_query("select * from product_product;")
    print(data)
    # put_query_in_queue(sql="select * from product_product;",param=None)
    # put_query_in_queue(sql="select * from product_product;",param=None)
    # put_query_in_queue(sql="select * from product_product;",param=None)