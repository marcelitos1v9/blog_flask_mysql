from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.like import Like, db
from models.news import News

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/news/<int:news_id>/like', methods=['POST'])
@login_required
def like_news(news_id):
    """Adiciona ou remove uma curtida em uma notícia"""
    news = News.query.get_or_404(news_id)
    
    # Verifica se o usuário já curtiu a notícia
    existing_like = Like.query.filter_by(
        user_id=current_user.id,
        news_id=news_id
    ).first()
    
    if existing_like:
        # Remove a curtida
        db.session.delete(existing_like)
        action = 'unliked'
    else:
        # Adiciona nova curtida
        new_like = Like(user_id=current_user.id, news_id=news_id)
        db.session.add(new_like)
        action = 'liked'
    
    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'action': action,
            'likes_count': len(news.likes)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@likes_bp.route('/news/<int:news_id>/likes', methods=['GET'])
def get_news_likes(news_id):
    """Retorna o número de curtidas de uma notícia"""
    news = News.query.get_or_404(news_id)
    return jsonify({
        'likes_count': len(news.likes),
        'user_liked': current_user.is_authenticated and 
                     Like.query.filter_by(
                         user_id=current_user.id,
                         news_id=news_id
                     ).first() is not None
    }) 