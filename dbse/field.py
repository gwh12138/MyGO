from dbse.connection import *


def add_field(field_name, size, crop_class,
              latitude, longitude, N, P, K, pH, length, width) -> int or None:
    """
    Add a new field
    :return: field_id 添加成功 0 添加失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = ("INSERT INTO field (field_name,size,crop_class,latitude,longitude,N,P,K,pH,length,width) VALUES ("
               "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        cursor.execute(sql, (field_name, size, crop_class, latitude, longitude, N, P, K, pH, length, width))
        db.commit()
        if cursor.rowcount == 0:
            return 0
        return cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def del_field(field_id) -> bool or None:
    """
    Delete a field
    :return: True 删除成功 False 删除失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM field WHERE field_id = %s"
        cursor.execute(sql, field_id)
        db.commit()
        if cursor.rowcount == 0:
            return False
        return True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)


def change_field(field_id, field_name=None, size=None, crop_class=None,
                 latitude=None, longitude=None, N=None, P=None, K=None, pH=None, length=None,
                 width=None) -> bool or None:
    """
    Change field information
    :return: True 修改成功 False 修改失败 None 出错
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"field_name": field_name, "size": size, "crop_class": crop_class,
                  "latitude": latitude, "longitude": longitude,
                  "N": N, "P": P, "K": K, "pH": pH, "length": length, "width": width}

        update_parts = [f"{key} = %s" for key, value in params.items() if value is not None]
        if update_parts:
            sql = f"UPDATE field SET {', '.join(update_parts)} WHERE field_id = %s"
            cursor.execute(sql, [value for key, value in params.items() if value is not None] + [field_id])
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


def search_field(field_id=None, field_name=None, size=None, crop_class=None,
                 latitude=None, longitude=None, N=None, P=None, K=None, pH=None, length=None,
                 width=None) -> list or None:
    """
    Search field information
    :return: [(field_id, field_name, size, crop_class, latitude, longitude, N, P, K, pH, length, width), ...]
    """
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        params = {"field_id": field_id, "field_name": field_name, "size": size, "crop_class": crop_class,
                  "latitude": latitude, "longitude": longitude,
                  "N": N, "P": P, "K": K, "pH": pH, "length": length, "width": width}

        query_parts = [f"{key} = %s" for key, value in params.items() if value is not None and value != '']
        if query_parts:
            sql = f"SELECT * FROM field WHERE {' AND '.join(query_parts)}"
            values = tuple(value for value in params.values() if value is not None and value != '')
            cursor.execute(sql, values)
        else:
            sql = "SELECT * FROM field"
            cursor.execute(sql)

        result = cursor.fetchall()
        return result

    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        close_db_connection(db)
