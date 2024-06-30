from dbse.connection import *


def add_employee_info(user_id, real_name=None, sex=None, telephone=None,
                      birthday=None, work_experience=None, profile=None) -> int or None:
    """
    Add a new employee info
    :param user_id:
    :param real_name:
    :param sex
    :param telephone:
    :param birthday:
    :param work_experience:
    :param profile:
    :return: user_id 添加成功 0 添加失败 None 出错
    """
    db = None
    result = 0
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = (
            "INSERT INTO employee_info (user_id, real_name, sex, telephone, birthday, work_experience, "
            "profile) VALUES ("
            "%s, %s, %s,%s, %s, %s, %s)")
        cursor.execute(sql, (user_id, real_name, sex, telephone, birthday, work_experience, profile))
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


def del_employee_info(user_id) -> bool or None:
    """
    Delete an employee info
    :param user_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM employee_info WHERE user_id = %s"
        cursor.execute(sql, user_id)
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_employee_info(user_id=None, real_name=None, sex=None, telephone=None, birthday=None, work_experience=None,
                         profile=None) -> bool or None:
    """
    Change an employee info
    :param user_id:
    :param real_name:
    :param sex
    :param telephone:
    :param birthday:
    :param work_experience:
    :param profile:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {'real_name': real_name, 'sex': sex, 'telephone': telephone, 'birthday': birthday,
                  'work_experience': work_experience, 'profile': profile}

        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None]

        if update_parts:
            sql = "UPDATE employee_info SET " + ", ".join(update_parts) + " WHERE user_id = %s"
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


def search_employee_info(user_id=None, real_name=None, sex=None, telephone=None, birthday=None, work_experience=None,
                         profile=None) -> list or None:
    """
    Search employee info
    :param sex:
    :param user_id:
    :param real_name:
    :param telephone:
    :param birthday:
    :param work_experience:
    :param profile:
    :return: [(user_id, real_name, sex, telephone, birthday, work_experience, profile), ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {'user_id': user_id, 'real_name': real_name, 'sex': sex, 'telephone': telephone,
                  'birthday': birthday, 'work_experience': work_experience, 'profile': profile}
        select_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != '']
        if select_parts:
            sql = "SELECT * FROM employee_info WHERE " + " AND ".join(select_parts)
            values = tuple(value for value in params.values() if value is not None and value != '')
            cursor.execute(sql, values)
        else:
            sql = "SELECT * FROM employee_info"
            cursor.execute(sql)
        return cursor.fetchall()
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def add_employee_info_batch(employee_info_list: list) -> int or None:
    """
    Add a batch of employee info
    :param employee_info_list: [(user_id, real_name, sex, telephone, birthday, work_experience, profile), ...]
    :return: 1 全部添加成功 0 添加失败 None 出错
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = ("INSERT INTO employee_info (user_id, real_name,sex,telephone,birthday,work_experience,profile) VALUES ("
               "%s, %s, %s, %s, %s, %s, %s)")
        cursor.executemany(sql, employee_info_list)
        db.commit()
        if cursor.rowcount != len(employee_info_list):
            return 0
        return 1
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


