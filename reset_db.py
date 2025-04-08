from app import app, db
from models.user import User
from models.news import News
from models.comment import Comment
from models.gallery import Gallery

def reset_database():
    with app.app_context():
        # Remove todas as tabelas
        db.drop_all()
        
        # Cria todas as tabelas novamente
        db.create_all()
        
        # Cria um usuário admin padrão
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Commit as mudanças
        db.session.commit()
        
        print("Banco de dados recriado com sucesso!")

if __name__ == '__main__':
    reset_database() 