from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId

# mongoDB product 컬렉션에서 있는 일들
class User():
    # 상품 등록
    @staticmethod
    def insert_one(form_data):
        db = conn_mongodb()
        db.users.insert_one ({
            'email': form_data['email'],
            'password': form_data['password'],
            'created_at': int(datetime.now().timestamp()),
            'update_at': int(datetime.now().timestamp())
        })
