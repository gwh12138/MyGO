from secure import PasswordSecure
from dbapi import *


def add_account(user_name, password, role) -> int or None:
    """
    Add a new account
    :param user_name:
    :param password:
    :param role:
    :return: user_id 添加成功 None 添加失败
    """
    db = None
    result = 0
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if role is None:
            role = 'user'
        password = PasswordSecure.encryption(password)
        sql = "INSERT INTO account (user_name, password, permission) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_name, password, role))
        db.commit()
        result = cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
    return result


def del_account(user_id, password) -> bool or None:
    """
    Delete an account
    :param user_id:
    :param password:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        password = PasswordSecure.encryption(password)
        sql = "DELETE FROM account WHERE user_id = %s AND password = %s"
        cursor.execute(sql, (user_id, password))
        db.commit()
        if cursor.rowcount == 0:
            return False
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
    return True


def change_account(user_id, user_name=None, password=None, permission=None) -> bool or None:
    """
    Change account information
    :param user_id:
    :param user_name:
    :param password:
    :param permission:
    :return: True 添加成功 False 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()

        params = {'user_name': user_name, 'password': password, 'permission': permission}

        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        sql = "UPDATE account SET " + ", ".join(update_parts) + " WHERE user_id = %s"

        values = tuple(value for value in params.values() if value is not None) + (user_id,)

        cursor.execute(sql, values)
        db.commit()
        if cursor.rowcount == 0:
            return False
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
    return True


def search_account(user_id=None, user_name=None, password=None, permission=None) -> list or None:
    """
    Search account
    :param user_id:
    :param user_name:
    :param password:
    :param permission:
    :return: [(user_id, user_name, password, permission), ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()

        params = {'user_id': user_id, 'user_name': user_name, 'password': password, 'permission': permission}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        sql = "SELECT * FROM account WHERE " + " AND ".join(query_parts)

        values = tuple(value for value in params.values() if value is not None)

        cursor.execute(sql, values)
        result = cursor.fetchall()
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
