# -*- coding: utf-8 -*- 
# TIME     : 2021/3/23 23:16
# AUTHOR   : luo nan
# FILE     : test_pytest.py
# SOFTWARE : PyCharm
# FUNCTION :

import pytest


def test_a():
    print("------->test_a")
    assert 1


def test_b():
    print("------->test_b")
    assert 0


if __name__ == '__main__':
    pytest.main(['-s', 'test_pytest.py'])
    # pytest.main(['-q', 'test_pytest.py'])
