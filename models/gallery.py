from datetime import datetime
import os
import hashlib
from config.database import db

class Gallery(db.Model):
    __tablename__ = 'gallery'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    uploader = db.relationship('User', backref=db.backref('gallery', lazy=True))
    news = db.relationship('News', backref=db.backref('gallery_images', lazy=True))
    
    @staticmethod
    def generate_unique_filename(original_filename):
        # Gera um hash único baseado no timestamp e no nome original do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hash_object = hashlib.md5(f"{timestamp}_{original_filename}".encode())
        hash_hex = hash_object.hexdigest()[:8]
        
        # Mantém a extensão original do arquivo
        _, ext = os.path.splitext(original_filename)
        return f"{hash_hex}{ext}"
    
    def __repr__(self):
        return f'<Gallery {self.title}>' 