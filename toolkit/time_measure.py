# -*- coding: utf-8 -*- 
# TIME     : 2020/12/6 15:06
# AUTHOR   : luo nan
# FILE     : time_measure.py
# SOFTWARE : PyCharm
# FUNCTION :

import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def time_measure(func):
    @ wraps(func)
    def timer_func(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        time_elapse = (end_time - start_time) * 1000
        func_name = func.__name__
        if len(args) > 0 and hasattr(args[0], func_name):
            func_name = f'{args[0].__class__.__name__}.{func_name}'

        logger.info('[TIME MEASURE] execute function: {} took {:.3f}ms'.format(func_name, time_elapse))
        return res
    return timer_func
