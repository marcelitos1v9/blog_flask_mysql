from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models.comment import Comment
from models.news import News
from config.database import db

bp = Blueprint('comments', __name__)

@bp.route('/news/<int:news_id>/comment', methods=['POST'])
@login_required
def create_comment(news_id):
    news = News.query.get_or_404(news_id)
    content = request.form.get('content')
    
    if not content:
        flash('O comentário não pode estar vazio', 'danger')
        return redirect(url_for('news.view', id=news_id))
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        news_id=news_id
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        flash('Comentário adicionado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao adicionar comentário', 'danger')
    
    return redirect(url_for('news.view', id=news_id))

@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if current_user.is_admin or comment.user_id == current_user.id:
        try:
            db.session.delete(comment)
            db.session.commit()
            flash('Comentário removido com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao remover comentário', 'danger')
    else:
        flash('Você não tem permissão para excluir este comentário', 'danger')
    
    return redirect(url_for('news.view', id=comment.news_id)) 