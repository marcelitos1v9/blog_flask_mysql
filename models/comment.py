from datetime import datetime
from .database import db

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    
    # Relacionamentos
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    news = db.relationship('News', backref=db.backref('comments', lazy=True))
    
    def __repr__(self):
        return f'<Comment {self.id}>'
    
    @property
    def formatted_date(self):
        return self.created_at.strftime('%d/%m/%Y %H:%M') 