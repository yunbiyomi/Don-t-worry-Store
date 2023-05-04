from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId

# mongoDB product 컬렉션에서 있는 일들
class Product():
    # 상품 등록
    @staticmethod
    def insert_one(product, thumbnail_img_url, detail_img_url):
        db = conn_mongodb()
        db.products.insert_one ({
            'name' : product['name'],
            'price': product['price'],
            'description': product['description'],
            'thumbnail_img': thumbnail_img_url,
            'detail_img': detail_img_url,
            'user': 'admin',
            'created_at': int(datetime.now().timestamp()),
            'update_at': int(datetime.now().timestamp())
        })

    # 상품 리스트
    @staticmethod
    def find():
        db = conn_mongodb()
        products = db.products.find({})
        return products
    
    # 상품 삭제
    @staticmethod
    def delete_one(id):
        db = conn_mongodb()
        db.products.delete_one({'_id': ObjectId(id)})

    # 상품 수정
    @staticmethod
    def update_one(id, product, thumbnail_img_url, detail_img_url):
        db = conn_mongodb()

        new_product = {
            'name' : product['name'],
            'price': product['price'],
            'description': product['description'],
            'user': 'admin',
            'update_at': int(datetime.now().timestamp())
        }

        if thumbnail_img_url:
            new_product['thumbnail_img'] = thumbnail_img_url
        if detail_img_url:
            new_product['detail_img'] = detail_img_url

        db.products.update_one(
            {'_id': ObjectId(id)},
            {'$set': new_product}
        )

    # 상품 수정 페이지
    @staticmethod
    def find_one(id):
        db = conn_mongodb()
        product = db.products.find_one({'_id': ObjectId(id)})
        return product