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
        params = {"user_id": user_id, "check_in_state": check_in_state, "check_time": check_time}
        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None ]
        if update_parts:
            sql = f"UPDATE check_in SET {', '.join(update_parts)} WHERE check_in_id = %s"
            cursor.execute(sql, [value for key, value in params.items() if value is not None] + [check_in_id])
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


def search_check_in(check_in_id=None, user_id=None, check_in_state=None, check_time=None) -> list or None:
    """
    Search check_in
    :param check_in_id:
    :param user_id:
    :param check_in_state:
    :param check_time:
    :return: [(check_in_id, user_id, check_in_state, check_time), ...] 查询成功 None 查询失败
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"check_in_id": check_in_id, "user_id": user_id, "check_in_state": check_in_state, "DATE(check_time)": check_time}
        where_parts = [f"{key} = %s" for key, value in params.items() if value is not None ]
        if where_parts:
            sql = f"SELECT * FROM check_in WHERE {' AND '.join(where_parts)}"
            cursor.execute(sql, [value for key, value in params.items() if value is not None])
        else:
            sql = "SELECT * FROM check_in"
            cursor.execute(sql)
        return cursor.fetchall()
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)