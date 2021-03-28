# -*- coding: utf-8 -*- 
# TIME     : 2020/11/30 21:42
# AUTHOR   : luo nan
# FILE     : basepath.py
# SOFTWARE : PyCharm
# FUNCTION :

import os


def get_base_path():
    """

    :return: project root base
    """
    base_path = os.path.dirname(__file__)

    return base_path


if __name__ == '__main__':
    path = get_base_path()
    print(path)