#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/6/28 下午3:10
# @File : connection.py
import pymysql

from app import app


# Get database connection
def get_db_connection():
    try:
        return pymysql.connect(
            host=app.config['DATABASE']['host'],
            user=app.config['DATABASE']['user'],
            passwd=app.config['DATABASE']['password'],
            db=app.config['DATABASE']['db']
        )
    except pymysql.Error as e:
        print('Error: ', e)
        return None


# Close database connection
def close_db_connection(db):
    """
    :param db:
    :return:
    """
    if db:
        try:
            db.close()
        except pymysql.Error as e:
            print('Error: ', e)
