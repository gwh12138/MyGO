from dbse.connection import *


def add_check_in(user_id,check_in_state,check_time) -> bool or None:
    """
    Add a new check_in
    :param user_id:
    :param check_in_state:
    :param check_time:
    :return: True 添加成功 False 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO check_in (user_id, check_in_state, check_time) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, check_in_state, check_time))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_check_in(check_in_id) -> bool or None:
    """
    Delete a check_in
    :param check_in_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM check_in WHERE check_in_id = %s"
        cursor.execute(sql, check_in_id)
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_check_in(check_in_id, user_id=None, check_in_state=None, check_time=None) -> bool or None:
    """
    Change a check_in
    :param check_in_id:
    :param user_id:
    :param check_in_state:
    :param check_time:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE check_in SET user_id = %s, check_in_state = %s, check_time = %s WHERE check_in_id = %s"
        cursor.execute(sql, (user_id, check_in_state, check_time, check_in_id))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)