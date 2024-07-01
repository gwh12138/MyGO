from connection import *
from dbse.plant_info import get_field_name, get_crop_name


def add_harvest_info(field_id, crop_id, harvest_date, harvest_weight) -> int or None:
    """
    Add a new harvest info
    :param field_id:
    :param crop_id:
    :param harvest_date:
    :param harvest_weight:
    :return: harvest_id 添加成功 0 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = ("INSERT INTO harvest_info (field_id, crop_id, harvest_date, yield) VALUES ("
               "%s, %s, %s, %s)")
        cursor.execute(sql, (field_id, crop_id, harvest_date, harvest_weight))
        db.commit()
        if cursor.rowcount == 0:
            return 0
        return cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_harvest_info(crop_id,field_id) -> bool or None:
    """
    Delete a harvest info
    :param crop_id:
    :param field_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM harvest_info WHERE crop_id = %s AND field_id = %s"
        cursor.execute(sql, (crop_id,field_id))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_harvest_info(field_id, crop_id, harvest_date=None, harvest_weight=None) -> bool or None:
    """
    Change harvest info
    :param field_id:
    :param crop_id:
    :param harvest_date:
    :param harvest_weight:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"harvest_date": harvest_date, "harvest_weight": harvest_weight}

        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        if update_parts :
            sql = f"UPDATE harvest_info SET {','.join(update_parts)} WHERE field_id = %s AND crop_id = %s"
            cursor.execute(sql, [value for key, value in params.items() if value is not None] + [field_id, crop_id])
            db.commit()
            if cursor.rowcount == 0:
                return False
            return True
        else :
            return False
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_harvest_info(field_id=None, crop_id=None, harvest_date=None, harvest_weight=None) -> list or None:
    """
    Search harvest info
    :param field_id:
    :param crop_id:
    :param harvest_date:
    :param harvest_weight:
    :return: [(field_id, crop_id, harvest_date, harvest_weight), ...]
    """
    db = None
    result = None
    field_name = None
    crop_name = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"field_id": field_id, "crop_id": crop_id, "harvest_date": harvest_date, "harvest_weight": harvest_weight}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != '']

        if query_parts:
            sql = "SELECT * FROM harvest_info WHERE " + " AND ".join(query_parts)
            cursor.execute(sql, [value for key, value in params.items() if value is not None and value != ''])
            result = cursor.fetchall()
            if field_id is not None:
                field_name = get_field_name(field_id)
            if crop_id is not None:
                crop_name = get_crop_name(crop_id)
            result_tmp = []
            for row in result:
                row = list(row)
                if field_name is not None:
                    row.insert(2, field_name)
                if crop_name is not None:
                    row.insert(2, crop_name)
                result_tmp.append(row)
            result = result_tmp
        else:
            sql = "SELECT * FROM harvest_info"
            result = cursor.execute(sql)

        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)