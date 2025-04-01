from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models.news import News
from models.user import db
import os
from werkzeug.utils import secure_filename

news_bp = Blueprint('news', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@news_bp.route('/')
def index():
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('news/index.html', news_list=news_list)

@news_bp.route('/<int:id>')
def view(id):
    news = News.query.get_or_404(id)
    return render_template('news/show.html', news=news)

@news_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem criar notícias.', 'danger')
        return redirect(url_for('news.index'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')
        
        if not title or not content:
            flash('Título e conteúdo são obrigatórios', 'warning')
            return redirect(url_for('news.create'))
            
        news = News(title=title, content=content, author=current_user)
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join('uploads', filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            news.image_path = image_path
            
        db.session.add(news)
        db.session.commit()
        
        flash('Notícia criada com sucesso!', 'success')
        return redirect(url_for('news.index'))
        
    return render_template('news/create.html')

@news_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem editar notícias.', 'danger')
        return redirect(url_for('news.index'))
        
    news = News.query.get_or_404(id)
    
    if request.method == 'POST':
        news.title = request.form.get('title')
        news.content = request.form.get('content')
        image = request.files.get('image')
        
        if image and allowed_file(image.filename):
            if news.image_path:
                old_image = os.path.join(current_app.config['UPLOAD_FOLDER'], news.image_path.split('/')[-1])
                if os.path.exists(old_image):
                    os.remove(old_image)
                    
            filename = secure_filename(image.filename)
            image_path = os.path.join('uploads', filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            news.image_path = image_path
            
        db.session.commit()
        flash('Notícia atualizada com sucesso!', 'success')
        return redirect(url_for('news.index'))
        
    return render_template('news/edit.html', news=news)

@news_bp.route('/<int:id>/delete')
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem excluir notícias.', 'danger')
        return redirect(url_for('news.index'))
        
    news = News.query.get_or_404(id)
    
    if news.image_path:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], news.image_path.split('/')[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
            
    db.session.delete(news)
    db.session.commit()
    
    flash('Notícia excluída com sucesso!', 'success')
    return redirect(url_for('news.index')) 