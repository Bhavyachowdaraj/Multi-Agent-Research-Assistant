from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from models.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat.chat_page'))
    return render_template('landing.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.chat_page'))
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already taken'}), 400
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify({'success': True, 'redirect': url_for('chat.chat_page')})
    return render_template('auth.html', mode='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.chat_page'))
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({'success': True, 'redirect': url_for('chat.chat_page')})
        return jsonify({'error': 'Invalid email or password'}), 401
    return render_template('auth.html', mode='login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@auth_bp.route('/upgrade')
@login_required
def upgrade():
    return render_template('upgrade.html')

@auth_bp.route('/upgrade/confirm', methods=['POST'])
@login_required
def upgrade_confirm():
    current_user.is_pro = True
    db.session.commit()
    return jsonify({'success': True, 'message': 'Upgraded to Pro!'})
