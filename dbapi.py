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
        sql = "SELECT field_name, field_pos, field_size, field_class, field_outcome, field_id FROM dmygo.field WHERE field_id=%s"
        cursor.execute(sql, (field_id,))
        result = cursor.fetchone()
        if len(result):
            return [{
                'field_name': result[0],
                'field_pos': result[1],
                'field_size': result[2],
                'field_class': result[3],
                'field_outcome': result[4],
                'field_id': result[5]
            }]
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
def add_product(product_class, product_name, product_price) -> int | None:
    """
    :param product_class:
    :param product_name:
    :param product_price:
    :return:
    """
    db = None
    product_id = 0
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.product_info (product_class, product_name, product_price) VALUES (%s, %s, %s)"
        cursor.execute(sql, (product_class, product_name, product_price))
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
def change_product(product_id, product_name, product_class, product_price) -> bool | None:
    """
    :param product_id:
    :param product_name:
    :param product_class:
    :param product_price:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.product_info SET product_name=%s, product_class=%s, product_price=%s WHERE product_id=%s"
        cursor.execute(sql, (product_name, product_class, product_price, product_id))
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
        sql = "SELECT product_id, product_class, product_name, product_price FROM dmygo.product_info"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            product_info = [{
                'product_id': row[0],
                'product_class': row[1],
                'product_name': row[2],
                'product_price': row[3]
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
        sql = "SELECT product_id, product_class, product_name, product_price FROM dmygo.product_info WHERE product_class=%s"
        cursor.execute(sql, (product_class,))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'product_class': row[1],
                'product_name': row[2],
                'product_price': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# get product_info by id
def get_product_by_id(product_id):
    """
    :param product_id:
    :return:
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_id, product_class, product_name, product_price FROM dmygo.product_info WHERE product_id=%s"
        cursor.execute(sql, (product_id,))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'product_class': row[1],
                'product_name': row[2],
                'product_price': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# add product_storage
def get_product_storage_list():
    db = None
    product_storage = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_storage.product_id, product_name,product_storage.field_id, field_name, product_quantity, product_price, product_state " \
              "FROM dmygo.product_storage, dmygo.product_info, dmygo.field " \
              "WHERE dmygo.product_storage.product_id = dmygo.product_info.product_id AND " \
              "dmygo.product_storage.field_id = dmygo.field.field_id" \

        cursor.execute(sql)
        result = cursor.fetchall()
        product_storage = [{
            'product_id': row[0],
            'product_name': row[1],
            'field_id': row[2],
            'field_name': row[3],
            'product_quantity': row[4],
            'product_price': row[5],
            'product_state': row[6]
        } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return product_storage


def get_product_storage(product_id, field_id):
    """
    :param product_id:
    :param field_id:
    :return: []
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_id, field_id, product_quantity, product_state FROM dmygo.product_storage " \
              "WHERE product_id=%s AND field_id=%s"
        cursor.execute(sql, (product_id, field_id))
        result = cursor.fetchall()
        if len(result) != 0:
            result = [{
                'product_id': row[0],
                'field_id': row[1],
                'product_quantity': row[2],
                'product_state': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# get product_storage by product_id
def get_product_storage_product_id(product_id, storage_id):
    """
    :param product_id:
    :param storage_id:
    :return:
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_id, field_id, product_quantity, product_state FROM dmygo.product_storage " \
              "WHERE product_id=%s AND field_id=%s"
        cursor.execute(sql, (product_id, storage_id))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'field_id': row[1],
                'product_quantity': row[2],
                'product_state': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# change product_storage
def change_product_storage(product_id, field_id, product_quantity, product_state):
    """
    :param product_id:
    :param field_id:
    :param product_quantity:
    :param product_state:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.product_storage SET product_quantity=%s, product_state=%s WHERE product_id=%s AND field_id=%s"
        cursor.execute(sql, (product_quantity, product_state, product_id, field_id))
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


# add product_storage
def add_product_storage(product_id, field_id, product_quantity, product_state):
    """
    :param product_id:
    :param field_id:
    :param product_quantity:
    :param product_state:
    :return: res: bool
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.product_storage (product_id, field_id, product_quantity, product_state) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (product_id, field_id, product_quantity, product_state))
        db.commit()

        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    return res


# del product_storage
def del_product_storage(product_id, field_id) -> bool | None:
    """
    :param product_id:
    :param field_id:
    :return: res: bool
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM dmygo.product_storage WHERE product_id=%s AND field_id=%s"
        cursor.execute(sql, (product_id, field_id))
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


# add goods
def add_goods(product_id, product_quantity, goods_price, goods_state):
    """
    :param product_id:
    :param product_quantity:
    :param goods_price:
    :param goods_state:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.goods_info (product_id, goods_quantity, goods_price, goods_state) VALUES (%s, %s, " \
              "%s, %s) "
        cursor.execute(sql, (product_id, product_quantity, goods_price, goods_state))
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


def del_goods(product_id):
    """
    :param product_id:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM dmygo.goods_info WHERE product_id=%s"
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


# change goods
def change_goods(product_id, product_quantity, goods_price,goods_state):
    """
    :param product_id:
    :param product_quantity:
    :param goods_price:
    :param goods_state:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "UPDATE dmygo.goods_info SET goods_quantity=%s, goods_price=%s, goods_state=%s WHERE product_id=%s"
        cursor.execute(sql, (product_quantity, goods_price, goods_state, product_id))
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


def get_goods_list():
    """
    :return: list
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_info.product_id, product_name, goods_quantity, goods_price, goods_state FROM dmygo.goods_info ,dmygo.product_info WHERE goods_info.product_id = product_info.product_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'product_name': row[1],
                'goods_quantity': row[2],
                'goods_price': row[3],
                'goods_state': row[4]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# harvest_product
def harvest_product(product_id, product_quantity):
    """
    :param product_id:
    :param product_quantity:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql_find_id = "SELECT product_id FROM dmygo.goods_info WHERE product_id=%s"
        cursor.execute(sql_find_id, (product_id,))
        if cursor.rowcount == 0:
            sql_get_price = "SELECT product_price FROM dmygo.product_info WHERE product_id=%s"
            cursor.execute(sql_get_price, (product_id,))
            product_price = cursor.fetchone()[0]
            sql_insert = "INSERT INTO dmygo.goods_info (product_id, goods_quantity, goods_price) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (product_id, product_quantity, product_price))
        else:
            sql = "UPDATE dmygo.goods_info SET goods_quantity=goods_quantity+%s WHERE product_id=%s"
            cursor.execute(sql, (product_quantity, product_id))
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


# get_goods_list_id
def get_goods_list_id(product_id):
    """
    :param product_id:
    :return:
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_id, goods_quantity, goods_price, goods_state FROM dmygo.goods_info WHERE product_id=%s"
        cursor.execute(sql, (product_id,))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'goods_quantity': row[1],
                'goods_price': row[2],
                'goods_state': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    return result


# get_sale_list
def get_sale_list():
    """
    :return: []
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT product_info.product_id, product_name, goods_quantity, goods_price FROM dmygo.goods_info,dmygo.product_info WHERE goods_state=1 AND goods_info.product_id=product_info.product_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'product_id': row[0],
                'product_name': row[1],
                'goods_quantity': row[2],
                'goods_price': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# sub_goods_quantity
def sub_goods_quantity(product_id, product_quantity):
    """
    :param product_id:
    :param product_quantity:
    :param goods_price:
    :param goods_state:
    :return: res: bool
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql_get_quantity = "SELECT goods_quantity FROM dmygo.goods_info WHERE product_id=%s"
        cursor.execute(sql_get_quantity, (product_id,))
        goods_quantity = cursor.fetchone()[0]
        if goods_quantity < product_quantity:
            return False
        sql = "UPDATE dmygo.goods_info SET goods_quantity=goods_quantity-%s WHERE product_id=%s"
        cursor.execute(sql, (product_quantity, product_id))
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


# new_orders
def new_orders(user_id, product_id, product_quantity):
    """
    :param user_id:
    :param product_id:
    :param product_quantity:
    :return:
    """
    orders_id = 0
    db = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "INSERT INTO dmygo.order (user_id, product_id, product_quantity) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, product_id, product_quantity))
        db.commit()
        orders_id = cursor.lastrowid
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return orders_id


# del_orders
def del_orders(orders_id):
    """
    :param orders_id:
    :return: res: bool
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "DELETE FROM dmygo.order WHERE order_id=%s"
        cursor.execute(sql, (orders_id,))
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


# get_orders_list
def get_orders_list():
    """
    :return: []
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT order_id, account.user_id,user_name, product_info.product_id, product_name, product_quantity, product_price FROM dmygo.order,dmygo.account,dmygo.product_info WHERE `order`.user_id=account.user_id AND `order`.product_id=product_info.product_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'order_id': row[0],
                'user_id': row[1],
                'user_name': row[2],
                'product_id': row[3],
                'product_name': row[4],
                'product_quantity': row[5],
                'product_price': row[6],
                'total_price': row[5] * row[6]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# get_orders_list_user_id
def get_orders_list_user_id(user_id):
    """

    :param user_id:
    :return:
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT order_id, user_id, product_info.product_id, product_name,product_quantity FROM dmygo.order ,dmygo.product_info WHERE user_id=%s AND dmygo.order.product_id=dmygo.product_info.product_id"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'order_id': row[0],
                'user_id': row[1],
                'product_id': row[2],
                'product_name': row[3],
                'product_quantity': row[4]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    finally:
        if db:
            close_db_connection(db)
    return result


# get_orders_list_product_id
def get_account_list():
    """

    :return:
    """
    db = None
    result = []
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql = "SELECT user_id, user_name, password,role FROM dmygo.account"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            return [{
                'user_id': row[0],
                'user_name': row[1],
                'user_password': row[2],
                'user_role': row[3]
            } for row in result]
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    return result


# get_account_list_user_id
def del_account_admin(user_id):
    """
    :param user_id:
    :return:
    """
    db = None
    res = False
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql_order = "DELETE FROM dmygo.order WHERE user_id=%s"
        cursor.execute(sql_order, (user_id,))
        sql = "DELETE FROM dmygo.account WHERE user_id=%s"
        cursor.execute(sql, (user_id,))
        db.commit()
        if cursor.rowcount > 0:
            res = True
    except pymysql.Error as e:
        print('Error: ', e)
        return None
    return res