from connection import *


def add_crop(crop_name, irrigation_per, crop_class, birth_cycle, yield_per) -> int or None:
    """
    Add a new crop
    :param irrigation_per:
    :param crop_name:
    :param crop_class:
    :param birth_cycle:
    :param yield_per:
    :return: crop_id 添加成功 0 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = ("INSERT INTO crop (crop_name, irrigation_per, crop_class, birth_cycle, yield_per) VALUES ("
               "%s, %s, %s, %s, %s)")
        cursor.execute(sql, (crop_name, irrigation_per, crop_class, birth_cycle, yield_per))
        db.commit()
        if cursor.rowcount == 0:
            return 0
        return cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_crop(crop_id) -> bool or None:
    """
    Delete a crop
    :param crop_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM crop WHERE crop_id = %s"
        cursor.execute(sql, crop_id)
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_crop(crop_id, crop_name=None, irrigation_per=None, crop_class=None, birth_cycle=None,
                yield_per=None) -> bool or None:
    """
    Change crop information
    :param irrigation_per:
    :param crop_id:
    :param crop_name:
    :param crop_class:
    :param birth_cycle:
    :param yield_per:
    :return:
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()

        params = {'crop_name': crop_name, 'irrigation': irrigation_per, 'crop_class': crop_class,
                  'birth_cycle': birth_cycle, 'yield_per': yield_per}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None]

        if query_parts:
            sql = "UPDATE crop SET " + ", ".join(query_parts) + " WHERE crop_id = %s"
            values = tuple(value for value in params.values() if value is not None) + (crop_id,)
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


def search_crop(crop_id=None, crop_name=None, irrigation = None,crop_class=None, birth_cycle=None, yield_per=None) -> list or None:
    """
    Search crop by crop_id, crop_name, crop_class, birth_cycle, yield_per
    :param irrigation:
    :param crop_id:
    :param crop_name:
    :param crop_class:
    :param birth_cycle:
    :param yield_per:
    :return: [(crop_id, crop_name, irrigation_per,crop_class, birth_cycle, yield_per), ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()

        params = {'crop_id': crop_id, 'crop_name': crop_name, 'irrigation_per':irrigation,'crop_class': crop_class, 'birth_cycle': birth_cycle,
                  'yield_per': yield_per}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None]

        if query_parts:
            sql = "SELECT * FROM crop WHERE " + " AND ".join(query_parts)
            values = tuple(value for value in params.values() if value is not None)
            cursor.execute(sql, values)
        else:
            sql = "SELECT * FROM crop"
            cursor.execute(sql)

        result = cursor.fetchall()
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
