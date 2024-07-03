from dbse.connection import *


def add_leave(user_id, leave_state, leave_date):
    """
    Add a leave
    :param user_id:
    :param leave_state:
    :param leave_date:
    :return: True 添加成功 False 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if leave_state is None or leave_state == '':
            leave_state = '申请中'
        sql = "INSERT INTO `leave` (user_id, leave_state, leave_date) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, leave_state, leave_date))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_leave(leave_id):
    """
    Delete a leave
    :param leave_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM `leave` WHERE leave_id = %s"
        cursor.execute(sql, leave_id)
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_leave(leave_id, user_id=None, leave_state=None, leave_date=None):
    """
    Change a leave
    :param leave_id:
    :param user_id:
    :param leave_state:
    :param leave_date:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if leave_state == '':
            leave_state = None
        params = {"user_id": user_id, "leave_state": leave_state, "leave_date": leave_date}
        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        sql = f"UPDATE `leave` SET {', '.join(update_parts)} WHERE leave_id = %s"
        cursor.execute(sql, tuple(
            [value for key, value in params.items() if value is not None and value != ""] + [leave_id]))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_leave(leave_id=None, user_id=None, leave_state=None, leave_date=None) -> list or None:
    """
    Search leave
    :param leave_id:
    :param user_id:
    :param leave_state:
    :param leave_date:
    :return: [(leave_id, user_id, leave_state, leave_date)...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if leave_state == '':
            leave_state = None
        params = {"leave_id": leave_id, "user_id": user_id, "leave_state": leave_state, "leave_date": leave_date}
        where_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        if where_parts:
            sql = f"SELECT * FROM `leave` WHERE {' AND '.join(where_parts)}"
            cursor.execute(sql, [value for key, value in params.items() if value is not None and value != ""])
        else:
            sql = "SELECT * FROM `leave`"
            cursor.execute(sql)
        res = cursor.fetchall()
        return res
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
