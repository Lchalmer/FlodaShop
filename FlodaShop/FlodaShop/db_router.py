# @Time: 2021-5-12  11:11
# @Author: chalmer
# @File: db_router.py.py
# @software: PyCharm
import random


class MasterSlaveDBRouter:
    """"数据库主从读写分离路由"""

    # 写操作
    def db_for_write(self, model, **hints):
        """随机选择一个主数据库写入数据"""
        # print('going------db_for_write')
        res = random.choice(['default', 'master02'])
        # print('going------db_for_write', res)
        return res

    # 读操作
    def db_for_read(self, model, **hints):
        """随机选择一个从数据库读取数据"""
        res = random.choice(['slave01', 'slave02'])
        # print('going------db_for_read', res)
        return res

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        # print('going-----allow_relation')
        return True
