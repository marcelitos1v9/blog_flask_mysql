from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from views.auth import auth_bp
from views.news import news_bp
from views.comments import bp as comments_bp
from views.likes import likes_bp
from views.gallery import gallery_bp
from models.user import User
from config.database import db, SQLALCHEMY_DATABASE_URI, recreate_database, init_db

app = Flask(__name__, 
    static_folder='static',  # Define a pasta static na raiz
    static_url_path='/static',
    template_folder='views/templates'  # Define a pasta de templates
)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-123456'  # Chave secreta para sessões
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Garantir que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registra os blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(comments_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(gallery_bp, url_prefix='/gallery')

# Função para verificar extensões permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota principal
@app.route('/')
def index():
    return redirect(url_for('news.index'))  # Redireciona para a página de notícias

if __name__ == '__main__':
    # Inicializa o banco de dados e cria as tabelas se necessário
    init_db(app)
    
    # Inicia o servidor
    app.run(host='0.0.0.0', port=4000, debug=True)
