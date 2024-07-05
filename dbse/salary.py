from dbse.connection import *


def add_salary(user_id, salary_date, basic_salary,
               performance_based_salary, total_salary, state='未发放') -> bool or None:
    """
    :param user_id:
    :param salary_date:
    :param basic_salary:
    :param performance_based_salary:
    :param total_salary:
    :param state:
    :return: True 添加成功 False 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = ("INSERT INTO salary (user_id, salary_date, basic_salary, performance_based_salary, total_salary, "
               "state) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (user_id, salary_date, basic_salary, performance_based_salary, total_salary, state))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_salary(user_id, salary_date) -> bool or None:
    """
    delete a salary
    :param user_id:
    :param salary_date:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM salary WHERE user_id = %s AND salary_date = %s"
        cursor.execute(sql, (user_id, salary_date))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_salary(user_id, salary_date, basic_salary=None,
                  performance_based_salary=None, total_salary=None, state=None) -> bool or None:
    """
    Change a salary
    :param user_id:
    :param salary_date:
    :param basic_salary:
    :param performance_based_salary:
    :param total_salary:
    :param state:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"basic_salary": basic_salary, "performance_based_salary": performance_based_salary,
                  "total_salary": total_salary, "state": state}
        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        sql = f"UPDATE salary SET {', '.join(update_parts)} WHERE user_id = %s AND salary_date = %s"
        cursor.execute(sql, tuple(
            [value for key, value in params.items() if value is not None and value != ""] + [user_id, salary_date]))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_salary(user_id=None, salary_date=None, basic_salary=None,
                  performance_based_salary=None, total_salary=None, state=None) -> list or None:
    """
    Search salary
    :param user_id:
    :param salary_date:
    :param basic_salary:
    :param performance_based_salary:
    :param total_salary:
    :param state:
    :return: [(user_id, salary_date, basic_salary, performance_based_salary, total_salary, state), ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"user_id": user_id, "salary_date": salary_date, "basic_salary": basic_salary,
                  "performance_based_salary": performance_based_salary, "total_salary": total_salary, "state": state}
        where_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != ""]
        if where_parts:
            sql = f"SELECT * FROM salary WHERE {' AND '.join(where_parts)}"
            cursor.execute(sql, [value for key, value in params.items() if value is not None and value != ""])
        else:
            sql = "SELECT * FROM salary"
            cursor.execute(sql)
        res = cursor.fetchall()
        return res
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
