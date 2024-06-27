import pymysql

from app import app


# Get database connection
def get_db_connection():
    try:
        return pymysql.connect(
            host=app.config['DATABASE']['host'],
            user=app.config['DATABASE']['user'],
            passwd=app.config['DATABASE']['password'],
            db=app.config['DATABASE']['db']
        )
    except pymysql.Error as e:
        print('Error: ', e)
        return None


# Close database connection
def close_db_connection(db):
    """
    :param db:
    :return:
    """
    if db:
        try:
            db.close()
        except pymysql.Error as e:
            print('Error: ', e)


# Get account from database
def get_account(user_name, password):
    """
    :param user_name: user name
    :param password: password
    :return: user_id,role
    """
    db = get_db_connection()
    cursor = db.cursor()
    sql = "SELECT user_id, role FROM dmygo.account WHERE user_name=%s AND password=%s"
    cursor.execute(sql, (user_name, password))
    result = cursor.fetchone()
    close_db_connection(db)
    if result:
        return result
    return None, None


# Add account to database
def add_account(user_name, password, role) -> None | int:
    """
    :param user_name:
    :param password:
    :param role:
    :return: user_id: int
    """
    db = None
    user_id = 0
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.account (user_name, password, role) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_name, password, role))

        db.commit()
        user_id = cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)

    return user_id


# Delete account from database
def del_account(user_name, password) -> None | bool:
    """
    :param user_name:
    :param password:
    :return: res: bool
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM dmygo.account WHERE user_name = %s AND password = %s"
        cursor.execute(sql, (user_name, password))

        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)

    return res


# Change account password
def change_account_password(user_name, password, new_password) -> bool | None:
    """
    :param new_password:
    :param user_name:
    :param password:
    :return: res: bool
    """
    res = False
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.account SET password=%s WHERE user_name=%s AND password=%s"
        cursor.execute(sql, (new_password, user_name, password))

        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return res


# Change account username
def change_account_username(user_name, password, new_username) -> bool | None:
    """
    :param new_username:
    :param user_name:
    :param password:
    :return: res: bool
    """
    res = False
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.account SET user_name=%s WHERE user_name=%s AND password=%s"
        cursor.execute(sql, (new_username, user_name, password))
        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return res


# Get all accounts
def get_all_accounts() -> list | None:
    """
    :return: accounts: list
    """
    db = None
    accounts = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT user_id, user_name, role FROM dmygo.account"
        cursor.execute(sql)
        result = cursor.fetchall()
        close_db_connection(db)
        for row in result:
            accounts.append({
                'user_id': row[0],
                'user_name': row[1],
                'role': row[2]
            })
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return accounts


# add field
def add_field(field_name, field_pos, size, field_class, field_outcome):
    """
    :param field_name:
    :param field_pos:
    :param size:
    :param field_class:
    :param field_outcome:
    :return: int
    """
    db = None
    field_id = 0
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.field (field_name, field_pos, field_size, field_class, field_outcome) VALUES (%s, " \
              "%s, %s, %s, %s) "
        cursor.execute(sql, (field_name, field_pos, size, field_class, field_outcome))
        db.commit()
        field_id = cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return field_id


# delete field
def del_field(field_id) -> bool | None:
    """
    :param field_id:
    :return:
    """
    res = False
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM dmygo.field WHERE field_id=%s"
        cursor.execute(sql, (field_id,))
        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return res


# change field
def change_field(field_id, field_name, field_pos, size, field_class, field_outcome) -> bool | None:
    """
    :param field_id:
    :param field_name:
    :param field_pos:
    :param size:
    :param field_class:
    :param field_outcome:
    :return: bool
    """
    if any(param in [None, ''] for param in [field_id, field_name, field_pos, size, field_class, field_outcome]):
        return False

    res = False
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.field SET field_name=%s, field_pos=%s, field_size=%s, field_class=%s, field_outcome=%s " \
              "WHERE field_id=%s "
        cursor.execute(sql, (field_name, field_pos, size, field_class, field_outcome, field_id))
        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return res


# get all fields
def get_field_list():
    """
    :return: fields: list
    """
    db = None
    fields = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT field_id, field_name, field_pos, field_size, field_class, field_outcome FROM dmygo.field"
        cursor.execute(sql)
        result = cursor.fetchall()
        fields = [{
            'field_id': row[0],
            'field_name': row[1],
            'field_pos': row[2],
            'field_size': row[3],
            'field_class': row[4],
            'field_outcome': row[5]
        } for row in result]

    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return fields


# get field by id
def get_field(field_id):
    """
    :param field_id:
    :return: field_name, field_pos, size, field_class, field_outcome
    """
    field_name = ''
    field_pos = ''
    size = ''
    field_class = ''
    field_outcome = ''
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT field_name, field_pos, field_size, field_class, field_outcome FROM dmygo.field WHERE field_id=%s"
        cursor.execute(sql, (field_id,))
        result = cursor.fetchone()
        if len(result) != 0:
            field_name = result[0]
            field_pos = result[1]
            size = result[2]
            field_class = result[3]
            field_outcome = result[4]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return field_name, field_pos, size, field_class, field_outcome


# get field class
def get_field_class(field_class):
    """
    :param field_class:
    :return:
    [
        {field_id, field_name, field_pos, size, field_class, field_outcome},
        ......
    ]
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT field_id, field_name, field_pos, field_size, field_class, field_outcome FROM dmygo.field " \
              "WHERE field_class=%s"
        cursor.execute(sql, (field_class,))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'field_id': row[0],
                'field_name': row[1],
                'field_pos': row[2],
                'field_size': row[3],
                'field_class': row[4],
                'field_outcome': row[5]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        result = None
    finally:
        if db:
            close_db_connection(db)
    return result


# add product_info
def add_product(product_class, product_name) -> int | None:
    """
    :param product_class:
    :param product_name:
    :return: product_id: int
    """
    db = None
    product_id = 0
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.product_info (product_class,product_name) VALUES (%s ,%s)"
        cursor.execute(sql, (product_class, product_name))
        db.commit()
        product_id = cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)

    return product_id


# del product_info
def del_product(product_id) -> bool | None:
    """
    :param product_id:
    :return: bool
    """
    res = False
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM dmygo.product_info WHERE product_id=%s"
        cursor.execute(sql, (product_id,))
        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return res


# change product_info
def change_product(product_id, product_name) -> bool | None:
    """
    :param product_id:
    :param product_name:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.product_info SET product_name=%s WHERE product_id=%s"
        cursor.execute(sql, (product_name, product_id))
        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return res


# get product_info
def get_product_list():
    """
    :return: product_info: list
    """
    db = None
    product_info = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_id, product_class, product_name FROM dmygo.product_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        product_info = [{
            'product_id': row[0],
            'product_class': row[1],
            'product_name': row[2]
        } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return product_info


# get product_info by class
def get_product_class(product_class):
    """
    :param product_class:
    :return:
    [
        {product_id, product_class, product_name}
        ......
    ]
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_id, product_class, product_name FROM dmygo.product_info WHERE product_class=%s"
        cursor.execute(sql, (product_class,))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'product_class': row[1],
                'product_name': row[2]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# add product_field