from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId


# 주문
class Order():
    @staticmethod
    def insert_one(product, form, user):
        db = conn_mongodb
        db.orders.insert_one({
            'status': 'pending',
            'product': product,
            'postcode': form['postcode'],
            'detail_adderss': form['detail_adderss'],
            'extra_address': form['extra_address'],
            'user_name': form['user_name'],
            'user_phone': form['user_phone'],
            'user': user,
            'created_at': int(datetime.now().timestamp()),
            'update_at': int(datetime.now().timestamp())
        })