from datetime import datetime
import os
from .database import db

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('news', lazy=True))
    
    def __repr__(self):
        return f'<News {self.title}>'
        
    @property
    def formatted_image_path(self):
        if not self.image_path:
            return None
        # Garante que o caminho use barras normais
        return self.image_path.replace('\\', '/')
        
    @property
    def formatted_date(self):
        if not self.created_at:
            return "Data não disponível"
        return self.created_at.strftime('%d/%m/%Y %H:%M') 