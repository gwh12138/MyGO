from dbse.secure import PasswordSecure
from dbse.connection import *


def add_account(user_name, password, role) -> int or None:
    """
    Add a new account
    :param user_name:
    :param password:
    :param role:
    :return: user_id 添加成功 0 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if role is None:
            role = 'user'
        password = PasswordSecure.encryption(password)
        sql = "INSERT INTO account (user_name, password, role) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_name, password, role))
        db.commit()
        if cursor.rowcount == 0:
            return 0
        result = cursor.lastrowid
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


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
        if password is not None:
            password = PasswordSecure.encryption(password)
        sql = "DELETE FROM account WHERE user_id = %s AND password = %s"
        cursor.execute(sql, (user_id, password))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_account(user_id, user_name=None, password=None, role=None) -> bool or None:
    """
    Change account information
    :param user_id:
    :param user_name:
    :param password:
    :param role:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if password is not None:
            password = PasswordSecure.encryption(password)
        params = {'user_name': user_name, 'password': password, 'role': role}

        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        if update_parts:
            sql = "UPDATE account SET " + ", ".join(update_parts) + " WHERE user_id = %s"
            values = tuple(value for value in params.values() if value is not None) + (user_id,)
            cursor.execute(sql, values)
            db.commit()
            if cursor.rowcount == 0:
                return False
            return True
        else:
            return False
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_account(user_id=None, user_name=None, role=None) -> list or None:
    """
    Search account
    :param user_id:
    :param user_name:
    :param role:
    :return: [(user_id, user_name, password, role), ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {'user_id': user_id, 'user_name': user_name, 'role': role}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        if query_parts:
            sql = "SELECT * FROM account WHERE " + " AND ".join(query_parts)
            values = tuple(value for value in params.values() if value is not None)
            cursor.execute(sql, values)
        else:
            sql = "SELECT * FROM account"
            cursor.execute(sql)
        result = cursor.fetchall()
        result = [list(row) for row in result]
        for row in result:
            row[2] = PasswordSecure.decryption(row[2])
        result = [tuple(row) for row in result]
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)


def add_account_batch(account_list: list) -> list or None:
    """
    Add multiple accounts
    :param account_list: [(user_name, password, role), ...]
    :return: [user_id, ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()

        account_list = [(user_name, PasswordSecure.encryption(password), role) for user_name, password, role in account_list]

        sql = "INSERT INTO account (user_name, password, role) VALUES (%s, %s, %s)"
        cursor.executemany(sql, account_list)
        db.commit()

        # 获取所有新插入的user_id
        result = [row[0] for row in cursor.fetchall()]
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


if __name__ == '__main__':
    # print(del_account(2, 'test'))
    # print(change_account(10, 'hdo', 'test', 'user'))
    print(search_account(role= 'user'))
    # print(add_account_batch([('test1', 'test1', 'user'), ('test2', 'test2', 'user')]))