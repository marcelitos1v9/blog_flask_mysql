from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.gallery import Gallery, db
from models.news import News

gallery_bp = Blueprint('gallery', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@gallery_bp.route('/')
def index():
    # Obtém todas as imagens ordenadas por data de criação
    images = Gallery.query.order_by(Gallery.created_at.desc()).all()
    # Obtém todas as notícias para o formulário de upload
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template('gallery/index.html', images=images, news=news)

@gallery_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem fazer upload.', 'danger')
        return redirect(url_for('gallery.index'))
        
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Nenhum arquivo selecionado', 'warning')
            return redirect(request.url)
            
        file = request.files['image']
        if file.filename == '':
            flash('Nenhum arquivo selecionado', 'warning')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Gera um nome de arquivo único
            filename = Gallery.generate_unique_filename(secure_filename(file.filename))
            
            # Garante que o diretório de uploads existe
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Salva o arquivo
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # Cria o registro no banco de dados
            gallery_item = Gallery(
                title=request.form.get('title', 'Sem título'),
                description=request.form.get('description'),
                image_path=f'uploads/{filename}',  # Caminho relativo para o template
                uploaded_by=current_user.id,
                news_id=request.form.get('news_id')  # ID da notícia vinculada
            )
            
            try:
                db.session.add(gallery_item)
                db.session.commit()
                flash('Imagem enviada com sucesso!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Erro ao salvar a imagem no banco de dados.', 'danger')
                # Remove o arquivo se houver erro no banco
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
            return redirect(url_for('gallery.index'))
            
        flash('Tipo de arquivo não permitido', 'danger')
    
    # Obtém todas as notícias para o formulário
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template('gallery/upload.html', news=news)

@gallery_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem excluir imagens.', 'danger')
        return redirect(url_for('gallery.index'))
        
    image = Gallery.query.get_or_404(id)
    
    # Remove o arquivo físico
    file_path = os.path.join(current_app.root_path, 'static', image.image_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    try:
        db.session.delete(image)
        db.session.commit()
        flash('Imagem excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir a imagem.', 'danger')
        
    return redirect(url_for('gallery.index'))

@gallery_bp.route('/news/<int:news_id>')
def news_gallery(news_id):
    # Obtém todas as imagens vinculadas a uma notícia específica
    images = Gallery.query.filter_by(news_id=news_id).order_by(Gallery.created_at.desc()).all()
    news = News.query.get_or_404(news_id)
    return render_template('gallery/news_gallery.html', images=images, news=news) 