# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 13:06
# AUTHOR   : luo nan
# FILE     : mkserver.py
# SOFTWARE : PyCharm
# FUNCTION :

import flask
import json
from flask import request, jsonify
from mockserver.readapidata import get_yaml_data_ruamel
import logging

logger = logging.getLogger(__name__)

"""
flask: web框架， 将当前文件作为一个服务
"""

# 创建服务
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# print(f"当前服务的配置信息：{app.config}")


@app.route('/user-app/api/v1/get_user_info', methods=['GET', 'POST'])
def user_info():
    if request.method != 'GET':
        err_msg = get_yaml_data_ruamel('err_method.yaml')
        return err_msg
    else:
        suc_msg = get_yaml_data_ruamel('d0002_student_info.yaml')
        return jsonify(suc_msg)


@app.route('/user-app/api/v2/get_user_info', methods=['GET', 'POST'])
def user_get_info():
    """
    # get 请求的参数处理
    :return:
    """
    # 获取所有参数
    req_param = request.values
    if request.method != 'GET':
        err_msg = get_yaml_data_ruamel('err_method.yaml')
        return err_msg
    else:
        return jsonify(req_param)


@app.route('/user-app/api/v3/get_user_info', methods=['GET', 'POST'])
def user_post_info():
    """
    # post 请求的参数处理
    :return:
    """
    # 获取post请求的表单数据支持form-data 和x-www-form-urlencoded
    # req_param = request.form

    # 获取解析json数据格式
    req_param = request.get_json()

    if request.method != 'POST':
        err_msg = get_yaml_data_ruamel('err_method.yaml')
        return err_msg
    else:
        return jsonify(req_param)


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port='50050')