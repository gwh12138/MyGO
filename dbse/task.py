from dbse.connection import *


def add_task(operate, crop_id, field_id,
             user_id, description, complete_time, task_state='未接收') -> bool or None:
    """
    add task
    :param operate:
    :param crop_id:
    :param field_id:
    :param user_id:
    :param description:
    :param complete_time:
    :param task_state:
    :return: True 添加成功 False 添加失败 None 错误
    """
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if task_state is None or task_state == '':
            task_state = '未接收'
        cursor.execute("INSERT INTO task(operate,crop_id,field_id,user_id,description,complete_time,task_state) "
                       "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                       (operate, crop_id, field_id, user_id, description, complete_time, task_state))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_task(task_id) -> bool or None:
    """
    delete a task
    :param task_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM task WHERE task_id = %s", (task_id,))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_task(task_id, operate=None, crop_id=None, field_id=None,
                user_id=None, description=None, complete_time=None, task_state=None) -> bool or None:
    """
    Change a task
    :param task_id:
    :param operate:
    :param crop_id:
    :param field_id:
    :param user_id:
    :param description:
    :param complete_time:
    :param task_state:
    :return: True 修改成功 False 修改失败 None 错误
    """
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"operate": operate, "crop_id": crop_id, "field_id": field_id,
                  "user_id": user_id, "description": description, "complete_time": complete_time,
                  "task_state": task_state}
        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        sql = f"UPDATE task SET {','.join(update_parts)} WHERE task_id = %s"
        cursor.execute(sql, [value for key, value in params.items() if value is not None] + [task_id])
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_task(task_id=None, operate=None, crop_id=None, field_id=None,
                user_id=None, description=None, complete_time=None, task_state=None) -> list or None:
    """
    search task
    :param task_id:
    :param operate:
    :param crop_id:
    :param field_id:
    :param user_id:
    :param description:
    :param complete_time:
    :param task_state:
    :return: list 查询成功 None 查询失败
    """
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if task_state is None or task_state == '':
            task_state = None
        params = {"task_id": task_id, "operate": operate, "crop_id": crop_id, "field_id": field_id,
                  "user_id": user_id, "description": description, "complete_time": complete_time,
                  "task_state": task_state}
        search_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        if search_parts:
            sql = f"SELECT * FROM task WHERE {' AND '.join(search_parts)}"
            cursor.execute(sql, [value for key, value in params.items() if value is not None and value != ""])
        else:
            sql = "SELECT * FROM task"
            cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_task_by_date(begin_date, end_date, user_id=None) -> list or None:
    """
    search task by date
    :param begin_date:
    :param end_date:
    :return: list 查询成功 None 查询失败
    """
    db = None
    result = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if user_id is None:
            if begin_date is not None and end_date is not None:
                sql = "SELECT * FROM task WHERE task.complete_time >= %s AND complete_time <= %s AND task_state='已完成' ORDER BY complete_time ASC"
                cursor.execute(sql, (begin_date, end_date))
            elif begin_date is not None:
                sql = "SELECT * FROM task WHERE complete_time >= %s AND task_state='已完成' ORDER BY complete_time ASC"
                cursor.execute(sql, (begin_date,))
            elif end_date is not None:
                sql = "SELECT * FROM task WHERE complete_time <= %s AND task_state='已完成' ORDER BY complete_time ASC"
                cursor.execute(sql, (end_date,))
            else:
                sql = "SELECT * FROM task WHERE task_state='已完成'ORDER BY complete_time ASC"
                cursor.execute(sql)
        else:
            if begin_date is not None and end_date is not None:
                sql = "SELECT * FROM task WHERE task.complete_time >= %s AND complete_time <= %s AND task_state='已完成' AND user_id = %s ORDER BY complete_time ASC"
                cursor.execute(sql, (begin_date, end_date,user_id))
            elif begin_date is not None:
                sql = "SELECT * FROM task WHERE complete_time >= %s AND task_state='已完成'AND user_id = %s ORDER BY complete_time ASC"
                cursor.execute(sql, (begin_date, end_date,user_id))
            elif end_date is not None:
                sql = "SELECT * FROM task WHERE complete_time <= %s AND task_state='已完成'AND user_id = %s ORDER BY complete_time ASC"
                cursor.execute(sql, (begin_date, end_date,user_id))
            else:
                sql = "SELECT * FROM task WHERE task_state='已完成'ORDER BY complete_time ASC"
                cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)