from flask import request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from .auth import check_login, redirect_to_longin_form, is_admin
from models.user import User


# 회원가입 페이지 API
@user.route('/form', methods=['GET'])
def form():
    return render_template('user_form.html')

# 회원가입 API
@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form_data = request.form 

    if not form_data['password'] == form_data['password_confirmation']:
        flash("비밀번호가 일치하지 않습니다.")
        return render_template('user_form.html')
    
    if not User.check_email(form_data['email']):
        flash("사용중인 이메일입니다.")
        return render_template('user_form.html')

    User.insert_one(form_data)
    return redirect(url_for('product.get_products'))



# 로그인 페이지 API
@user.route('/login', methods=['GET'])
def login_form():
    return render_template('user_login.html')

# 로그인 API
@user.route('/login', methods=['GET', 'POST'])
def login():
    form_data = request.form
    user = User.log_in(form_data)

    if not user:
        flash("이메일 주소 또는 비밀번호를 확인해주세요.")
        return render_template('user_login.html')
    else:
        session['user_id'] = str(user['_id'])
        if is_admin():
            session['is_admin'] = True
        
        return redirect(url_for('product.get_products'))



# 로그아웃
@user.route('/logout', methods=['GET'])
def logout():
    user = check_login()

    if not user:
        return redirect_to_longin_form()

    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('product.get_products'))