# -*- coding: utf-8 -*- 
# TIME     : 2020/11/30 22:34
# AUTHOR   : luo nan
# FILE     : op_xls.py
# SOFTWARE : PyCharm
# FUNCTION :

import os
import logging
import xlrd, xlwt
from xlutils.copy import copy
from basepath import get_base_path
from toolkit.time_measure import time_measure

logger = logging.getLogger(__name__)
xl_top_path = os.path.join(get_base_path(), "data", 'casedir')


class GetExcelInfo:

    def __init__(self, xl_name, sheet):
        """
        初始化
        :param xl_name:
        :param sheet:
        """
        self.xl_name = xl_name
        self.sheet = sheet
        self.xl_path = os.path.join(xl_top_path, self.xl_name)
        self.read_book = xlrd.open_workbook(self.xl_path)
        self.sheets = self.read_book.sheet_by_name(self.sheet)

    @time_measure
    def get_excel_info(self):
        """
        读取Excel，返回所有行信息到一个list
        :return:
        """
        value_list = []
        rows = self.sheets.nrows
        for i in range(rows):
            if i != 0:
                value_list.append(self.sheets.row_values(i))
                logger.info(i, self.sheets.row_values(i))
        return value_list

    def wt_excel_info(self, i, value):
        """

        :param i: 代表插入数据到第几行
        :param value: 代表我们要插入的值
        :return:
        """
        if i != 0:
            write_book = copy(self.read_book)  # 利用xlutils.copy下的copy函数复制
            sheet = write_book.get_sheet(self.sheet)
            sheet.write(i, 3, value)
            write_book.save(self.xl_path)
            return '写入成功！'


@time_measure
def res_to_xls(filename, data, sheet_name='testcase'):
    """

    :param filename: excel的名称
    :param data:   写入excel的数据 [] 列表格式
    :param sheet_name:  excel 的 sheet_name
    :return:
    """
    filename = os.path.join(xl_top_path, filename)
    list_table_header = ['用例编号', '用例名称', '接口路径', '请求方法', '请求数据', '返回结果']
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=False)

    # 写入表头
    for i in range(len(list_table_header)):
        sheet.write(0, i, list_table_header[i])

    # 写入数据
    row = 1
    for res in data:
        col = 0

        for c in res:
            sheet.write(row, col, c)
            col += 1
        row += 1
    workbook.save(filename)
    print(f"文件{filename}数据写入成功")


if __name__ == '__main__':
    # 插入一条数据，读出来验证读写方法的正确性
    # GetExcelInfo('userinfo.xls', 'testcase').wt_excel_info(1, 'PASS')
    p = GetExcelInfo('userinfo.xls', 'testcase')
    result = p.get_excel_info()
    print(result)

    data = [
        [
            'T0001',
            '验证用户信息1',
            '/user-app/api/v1/get_user_info',
            'get',
            '',
            'username'
        ],
        [
            'T0002',
            '验证用户信息2',
            '/user-app/api/v2/get_user_info',
            'get',
            'username=luonan&passwd=mima123&city=shanghai',
            'username'
        ]
    ]

    res_to_xls('test_rw_xls.xls',data)