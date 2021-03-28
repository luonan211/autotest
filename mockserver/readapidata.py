# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 12:19
# AUTHOR   : luo nan
# FILE     : readapidata.py
# SOFTWARE : PyCharm
# FUNCTION : 获取mock的数据

import os
import json
import logging
from ruamel import yaml
from basepath import get_base_path

logger = logging.getLogger(__name__)
path = os.path.join(get_base_path(), 'mockserver', 'data')


class ReadApiData:
    """
    # 读取API json格式的数据，返回dict格式的数据
    # 提供给flask使用
    """
    def __init__(self, filename):
        self.path = os.path.join(get_base_path(), 'mockserver', 'data')
        self.file = os.path.join(self.path, filename)

    def get_api_data(self):
        """

        :return: dict
        """
        try:
            with open(self.file, 'r', True, encoding='utf-8')as f:
                data = json.load(f)
        except Exception as e:
            logger.exception(f"caught an exception during execute get_api_data: {e}")
            return {}   # 不应该返回空字典的，增加排查问题的难度
        return data


def generate_yaml_doc_ruamel(yaml_file, dictdata):
    """
      # 在指定目录下生成指定名称的yaml文件
      # 输入的参数
      # yaml_file  文件名 str
      # dictdata   数据 dict
    """
    yaml_path = os.path.join(path, yaml_file)
    with open(yaml_path, 'w', encoding='utf-8')as f:
        yaml.dump(dictdata, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    print(f"数据写入成功，请核对数据{yaml_path}")


def get_yaml_data_ruamel(yaml_file):
    f1 = os.path.join(path, yaml_file)
    with open(f1, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
    return data


if __name__ == '__main__':
    wt_data = {'res_code': 0,
               'res_msg': 'success',
               'data':
                   [{'username': 'Mike', 'age': 18, 'sex': 'F'},
                    {'username': 'Lucy', 'age': 19, 'sex': 'M'},
                    {'username': 'LiMing', 'age': 17, 'sex': 'F'}
                    ]}
    # aa = get_yaml_data_ruamel("d0001_student_info.yaml")
    # print(aa)

    generate_yaml_doc_ruamel("d0003_student_info.yaml", wt_data)

    data = get_yaml_data_ruamel("d0003_student_info.yaml")
    print(type(data))
    print(data)

