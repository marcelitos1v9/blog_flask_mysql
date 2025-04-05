import os
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blog_news',
    'charset': 'utf8mb4'
}

# String de conexão para o SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

# Inicialização do SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    db.init_app(app)
    with app.app_context():
        # Verifica se o banco de dados existe
        if not database_exists():
            create_database()
        # Cria as tabelas se não existirem
        db.create_all()

def database_exists():
    """Verifica se o banco de dados existe"""
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{DB_CONFIG['database']}'")
            exists = cursor.fetchone() is not None
            
        connection.close()
        return exists
        
    except pymysql.Error as e:
        print(f"Erro ao verificar banco de dados: {e}")
        return False

def create_database():
    """Cria o banco de dados se não existir"""
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            connection.commit()
            
        connection.close()
        print("Banco de dados criado com sucesso!")
        
    except pymysql.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
        raise

def recreate_database():
    """Recria o banco de dados e todas as tabelas"""
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
            connection.commit()
            
        connection.close()
        print("Banco de dados recriado com sucesso!")
        
    except pymysql.Error as e:
        print(f"Erro ao recriar o banco de dados: {e}")
        raise 