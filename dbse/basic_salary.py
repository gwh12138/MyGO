from connection import *


def add_basic_salary(role_name, role_salary) -> bool or None:
    """
    Add a new basic salary
    :param role_name:
    :param role_salary:
    :return:
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if (role_name is None) or (role_salary is None):
            return None
        sql = "INSERT INTO basic_salary (role_name, role_salary) VALUES (%s, %s)"
        cursor.execute(sql, (role_name, role_salary))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_basic_salary(role_name) -> bool or None:
    """
    Delete a basic salary
    :param role_name:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if role_name is None:
            return None
        sql = "DELETE FROM basic_salary WHERE role_name = %s"
        cursor.execute(sql, role_name)
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_basic_salary(role_name, role_salary) -> bool or None:
    """
    Change a basic salary
    :param role_name:
    :param role_salary:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if role_name is None:
            return None
        sql = "UPDATE basic_salary SET role_salary = %s WHERE role_name = %s"
        cursor.execute(sql, (role_salary, role_name))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_basic_salary(role_name=None, role_salary=None) -> list or None:
    """
    Search basic salary
    :param role_name:
    :param role_salary:
    :return: [(role_name, role_salary), ...] 查询成功 None 查询失败
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"role_name": role_name, "role_salary": role_salary}
        where_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        if where_parts:
            sql = f"SELECT * FROM basic_salary WHERE {' AND '.join(where_parts)}"
            cursor.execute(sql, [value for key, value in params.items() if value is not None and value != ""])
        else:
            sql = "SELECT * FROM basic_salary"
            cursor.execute(sql)
        res = cursor.fetchall()
        return res
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
