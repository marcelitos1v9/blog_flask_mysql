from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor, preencha todos os campos', 'warning')
            return redirect(url_for('auth.login'))
            
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('news.index'))
            
        flash('Usuário ou senha inválidos', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('Por favor, preencha todos os campos', 'warning')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe', 'warning')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado', 'warning')
            return redirect(url_for('auth.register'))
            
        # Verifica se é o primeiro usuário
        is_first_user = User.query.count() == 0
        
        try:
            user = User(
                username=username,
                email=email,
                is_admin=is_first_user
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            if is_first_user:
                flash('Conta de administrador criada com sucesso!', 'success')
            else:
                flash('Registro realizado com sucesso!', 'success')
                
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar usuário. Tente novamente.', 'danger')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'info')
    return redirect(url_for('news.index')) 