from connection import *


def add_plant_info(crop_id, field_id, plant_date, crop_state, size, longitude, latitude) -> int or None:
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


def change_plant_info(field_id, crop_id, plant_date=None, crop_state=None, size=None, longitude=None,
                      latitude=None) -> bool or None:
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
        params = {"plant_date": plant_date, "crop_state": crop_state, "size": size, "longitude": longitude,
                  "latitude": latitude}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None]

        if query_parts:
            sql = f"UPDATE plant_info SET {','.join(query_parts)} WHERE field_id = %s AND crop_id = %s"
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


def get_field_name(field_id) -> str or None:
    """
    Get field name
    :param field_id:
    :return: field_name
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT field_name FROM field WHERE field_id = %s"
        cursor.execute(sql, (field_id,))
        if cursor.rowcount == 0:
            return None
        return cursor.fetchone()[0]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def get_crop_name(crop_id) -> str or None:
    """
    Get crop name
    :param crop_id:
    :return: crop_name
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT crop_name FROM crop WHERE crop_id = %s"
        cursor.execute(sql, (crop_id,))
        if cursor.rowcount == 0:
            return None
        return cursor.fetchone()[0]
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
    :return: [(crop_id, field_id, crop_name, field_name, plant_date, crop_state, size, longitude, latitude
    """
    db = None
    result = None
    field_name = None
    crop_name = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"field_id": field_id, "crop_id": crop_id, "plant_date": plant_date, "crop_state": crop_state,
                  "size": size, "longitude": longitude, "latitude": latitude}
        query_parts = [f"plant_info.{key} = %s" for key, value in params.items() if value is not None and value != '']
        if query_parts:
            sql = "SELECT * FROM plant_info WHERE " + " AND ".join(query_parts)
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
            sql = ("SELECT plant_info.crop_id, plant_info.field_id, crop.crop_name, field.field_name, "
                   "plant_info.plant_date, plant_info.crop_state, plant_info.size, plant_info.longitude, plant_info.latitude "
                   "FROM plant_info "
                   "INNER JOIN crop ON plant_info.crop_id = crop.crop_id "
                   "INNER JOIN field ON plant_info.field_id = field.field_id")
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)

