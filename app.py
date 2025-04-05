from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models.user import User
from models.database import db
import os
import pymysql
from sqlalchemy import create_engine

app = Flask(__name__, 
    static_folder='static',  # Define a pasta static na raiz
    static_url_path='/static',
    template_folder='views/templates'  # Define a pasta de templates
)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/blog_news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-123456'  # Chave secreta para sessões
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Garantir que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def recreate_database():
    """Recria o banco de dados e todas as tabelas"""
    try:
        # Conecta ao MySQL sem selecionar banco de dados
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Remove o banco de dados se existir
            cursor.execute("DROP DATABASE IF EXISTS blog_news")
            connection.commit()
            
            # Cria o banco de dados
            cursor.execute("CREATE DATABASE blog_news")
            connection.commit()
            
            # Seleciona o banco de dados
            cursor.execute("USE blog_news")
            
            # Cria as tabelas usando SQLAlchemy
            with app.app_context():
                db.create_all()
                
        connection.close()
        print("Banco de dados e tabelas recriados com sucesso!")
        
    except pymysql.Error as e:
        print(f"Erro ao recriar o banco de dados: {e}")
        raise

def create_database():
    """Cria o banco de dados se não existir"""
    try:
        # Conecta ao MySQL sem selecionar banco de dados
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Cria o banco de dados se não existir
            cursor.execute("CREATE DATABASE IF NOT EXISTS blog_news")
            connection.commit()
            
            # Seleciona o banco de dados
            cursor.execute("USE blog_news")
            
            # Cria as tabelas usando SQLAlchemy
            with app.app_context():
                db.create_all()
                
        connection.close()
        print("Banco de dados e tabelas criados com sucesso!")
        
    except pymysql.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
        raise

# Inicialização do banco de dados
db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registro dos blueprints
from views.auth import auth_bp
from views.news import news_bp
from views.gallery import gallery_bp
from views.comments import bp as comments_bp

# Registra os blueprints com URLs específicas
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(gallery_bp, url_prefix='/gallery')
app.register_blueprint(comments_bp)

# Rota principal
@app.route('/')
def index():
    return redirect(url_for('news.index'))  # Redireciona para a página de notícias

if __name__ == '__main__':
    # Recria o banco de dados e as tabelas
    recreate_database()
    
    # Inicia o servidor
    app.run(host='0.0.0.0', port=4000, debug=True)
