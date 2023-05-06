from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from .blueprint import product
from .blueprint import user
from .auth import check_login, redirect_to_longin_form
from models.product import Product
from models.order import Order
from datetime import datetime
import os

# 상품 등록 페이지 API
@product.route('/form', methods=['GET'])
def form():
    if not session.get('user_id'):
        return redirect(url_for('product.get_products'))
    
    return render_template('product_form.html')

@product.route('/regist', methods=['GET', 'POST'])
def regist():
    if not session.get('user_id'):
        return redirect(url_for('product.get_products'))
    
    # 전달받은 상품 정보
    form_data = request.form
    thumbnail_img = request.files.get('thumbnail_img')
    detail_img = request.files.get('detail_img')
    thumbnail_img_url = ""
    detail_img_url = ""

    if thumbnail_img:
        thumbnail_img_url = _upload_file(thumbnail_img)
    if detail_img:
        detail_img_url = _upload_file(detail_img)

    # 상품 정보 저장
    Product.insert_one(form_data, thumbnail_img_url, detail_img_url)
    return redirect(url_for('product.get_products'))



# 상품 리스트 조회 페이지 API
@product.route('/list', methods=['GET'])
def get_products():
    # 상품 리스트 정보 (mongoDB products 컬렉션에 있는 documents)
    products = Product.find()
    return render_template('products.html', products=products)



# 상품 삭제 API
@product.route('/<product_id>/delete', methods=['GET'])
def delete(product_id):
    if not session.get('user_id'):
        return redirect(url_for('product.get_products'))
    
    Product.delete_one(product_id)
    return redirect(url_for('product.get_products'))



# 상품 수정 페이지 API
@product.route('/<product_id>/edit', methods=['GET'])
def edit(product_id):
    if not session.get('user_id'):
        return redirect(url_for('product.get_products'))
    
    product = Product.find_one(product_id)
    return render_template('product_edit.html', product=product)



# 상품 수정 API
@product.route('/<product_id>/update', methods=['GET', 'POST'])
def update(product_id):
    if not session.get('user_id'):
        return redirect(url_for('product.get_products'))
    
    form_data = request.form
    thumbnail_img = request.files.get('thumbnail_img')
    detail_img = request.files.get('detail_img')
    thumbnail_img_url = ""
    detail_img_url = ""

    if thumbnail_img:
        thumbnail_img_url = _upload_file(thumbnail_img)
    if detail_img:
        detail_img_url = _upload_file(detail_img)

    Product.update_one(product_id, form_data, thumbnail_img_url, detail_img_url)
    return redirect(url_for('product.get_products'))



# 상품 상세 정보 페이지 API
@product.route('/<product_id>/detail', methods=['GET'])
def detail(product_id):
    product = Product.find_one(product_id)
    return render_template('product.html', product=product)


# 상품 주문 페이지 API
@product.route('/<product_id>/order', methods=['GET'])
def order_form(product_id):
    product = Product.find_one(product_id)
    return render_template('order_form.html', product=product)


# 주문 생성 API
@product.route('/<product_id>/order', methods=['GET', 'POST'])
def order(product_id):
    user = check_login()
    if not user:
        return redirect_to_longin_form()

    product = Product.find_one(product_id)
    form_data = request.form

    Order.insert_one(product, form_data, user)

    return render_template('payment_complete.html')



# 이미지 저장
def _upload_file(img_file):
    timestamp = str(datetime.now().timestamp())
    filename = timestamp + '_' + secure_filename(img_file.filename)
    image_path = f'./static/uploads'
    os.makedirs(image_path, exist_ok=True)
    img = os.path.join(image_path, filename)
    img_file.save(img)

    return f'/static/uploads/' + filename