from connection import *


def add_plant_info(crop_id, field_id, plant_date,crop_state, size, longitude, latitude) -> int or None:
    """
    Add a new plant info
    :param crop_state:
    :param crop_id:
    :param field_id:
    :param plant_date:
    :param size:
    :param longitude:
    :param latitude:
    :return: plant_id 添加成功 0 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = ("INSERT INTO plant_info (crop_id, field_id, plant_date, crop_state,size,longitude,latitude) VALUES ("
               "%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (crop_id, field_id, plant_date, crop_state, size, longitude, latitude))
        db.commit()
        if cursor.rowcount == 0:
            return 0
        return cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_plant_info(crop_id, field_id) -> bool or None:
    """
    Delete a plant info
    :param crop_id:
    :param field_id:
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM plant_info WHERE crop_id = %s AND field_id = %s"
        cursor.execute(sql, (crop_id, field_id))
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_plant_info(field_id, crop_id, plant_date=None, crop_state=None, size=None, longitude=None, latitude=None) -> bool or None:
    """
    Change plant info
    :param crop_state:
    :param field_id:
    :param crop_id:
    :param plant_date:
    :param size:
    :param longitude:
    :param latitude:
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"plant_date": plant_date, "crop_state":crop_state, "size": size, "longitude": longitude, "latitude": latitude}

        quary_parts = [f"{key} = %s" for key, value in params.items() if value is not None]

        if quary_parts:
            sql = f"UPDATE plant_info SET {','.join(quary_parts)} WHERE field_id = %s AND crop_id = %s"
            cursor.execute(sql, [value for key, value in params.items() if value is not None] + [field_id, crop_id])
            db.commit()
            if cursor.rowcount == 0:
                return False
            return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def search_plant_info(field_id=None, crop_id=None, plant_date=None, crop_state=None, size=None, longitude=None,
                      latitude=None) -> list or None:
    """
    Search plant info
    :param crop_state:
    :param field_id:
    :param crop_id:
    :param plant_date:
    :param size:
    :param longitude:
    :param latitude:
    :return: list 查询成功 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"field_id": field_id, "crop_id": crop_id, "plant_date": plant_date, "crop_state":crop_state,
                  "size": size, "longitude": longitude, "latitude": latitude}
        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        if query_parts:
            sql = "SELECT * FROM plant_info WHERE " + " AND ".join(query_parts)
            cursor.execute(sql, [value for key, value in params.items() if value is not None])
        else:
            sql = "SELECT * FROM plant_info"
            cursor.execute(sql)
        return cursor.fetchall()
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
