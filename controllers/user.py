from flask import request, render_template, redirect, url_for
from .blueprint import user
from models.user import User


# 회원가입 페이지 API
@user.route('/form', methods=['GET'])
def form():
    return render_template('user_form.html')

# 회원가입 API
@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form_data = request.form

    User.insert_one(form_data)
    return "회원가입이 성공적으로 완료되었습니다."