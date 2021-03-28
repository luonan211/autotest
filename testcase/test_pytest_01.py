# -*- coding: utf-8 -*- 
# TIME     : 2020/12/10 22:33
# AUTHOR   : luo nan
# FILE     : test_pytest_01.py
# SOFTWARE : PyCharm
# FUNCTION :

import pytest


def add(x, y):
    return x+y


def test_add_01():
    assert add(2, 8) == 10


def test_add_02():
    assert add(3, 7) == 9


if __name__ == '__main__':
    pytest.main(['-q', 'test_pytest_01.py'])