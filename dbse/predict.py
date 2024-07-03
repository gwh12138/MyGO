from dbse.connection import *


def predict_harvest(crop_id) -> list or None:
    """

    :param crop_id:
    :return: N,P,K,ph,Harvest_Weight
    """
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql_one = "SELECT field_id,`yield` FROM harvest_info WHERE crop_id = %s"
        cursor.execute(sql_one, crop_id)
        result_one = cursor.fetchall()
        tmp = [row[1] for row in result_one]
    except pymysql.Error as e:
        print('One_Error: ', e)
        return None
    finally:
        close_db_connection(db)

    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql_two = "SELECT N,P,K,ph FROM field WHERE field_id = %s"
        cursor.execute(sql_two, result_one[0])
        result_two = cursor.fetchall()
    except pymysql.Error as e:
        print('Two_Error: ', e)
        return None
    finally:
        close_db_connection(db)

    return result_two, tmp
