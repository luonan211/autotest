# -*- coding: utf-8 -*- 
# TIME     : 2020/12/1 22:24
# AUTHOR   : luo nan
# FILE     : getenvconfig.py
# SOFTWARE : PyCharm
# FUNCTION :

import os
import yaml
import logging
import basepath
logger = logging.getLogger(__name__)

BASE = basepath.get_base_path()

ENV_CONFIG = os.path.join(BASE, 'config', 'env.yaml')


def get_env_config(file=ENV_CONFIG):
    try:
        if not os.path.isfile(file):
            logger.debug(f"{file}不是一个文件，请核对配置文件的路径")
        else:
            with open(file, 'r', encoding='utf-8')as f:
                config = yaml.safe_load(f)
            return config
    except Exception as e:
        logger.exception(f"异常{e}")
        return []


def get_url():
    """获取配置文件中url"""
    config = get_env_config()
    # print(config)
    scheme = config.get('HTTP', {}).get('shceme', 'http')
    host = config.get('HTTP', {}).get('host', '')
    port = config.get('HTTP', {}).get('port', '50060')
    return scheme+"://"+host+":"+str(port)


def get_email_config():
    """获取配置文件中邮件配置"""
    env_config = get_env_config()
    email_config = env_config.get("EMAIL_QQ",{})
    return email_config


if __name__ == '__main__':
    # config = get_env_config()
    # print(config)
    # email = get_email_config()
    # print(type(email))
    # print(email)

    url =get_url()
    print(url)