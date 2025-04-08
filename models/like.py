from datetime import datetime
from config.database import db

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    news = db.relationship('News', backref=db.backref('likes', lazy=True, cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<Like {self.id}>' 