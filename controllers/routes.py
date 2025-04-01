from flask import render_template, request, redirect, url_for, flash, session
# Importando o Model
from models.database import db, Game, Usuario
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json
# Importando biblioteca para Hash de Senha
from werkzeug.security import generate_password_hash, check_password_hash
# Biblioteca para editar a Flash Message
from markupsafe import Markup # Inclui HTML dentro das Flash Messages

jogadores = []

gamelist = [{'titulo': 'CS-GO',
             'ano': 2012,
             'categoria': 'FPS Online'}]


def init_app(app):
    # Função para verificar se o usuário está logado
    @app.before_request
    def check_auth():
        # rotas que nao precisam de autenticação
        whitelist = ['login', 'caduser','home','logout']
        #liberando rotas e oque vem de static
        if request.endpoint in whitelist or (request.endpoint and request.endpoint.startswith('static')):
            return
        
        # se o usuário não está logado, redireciona para a página de login  
        if not session.get('user_id'):
            return redirect(url_for('login'))
       
    @app.route('/')
    # View function -> função de visualização
    def home():
        return render_template('index.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logout realizado com sucesso!', 'success')
        return redirect(url_for('home'))

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        # Verifica se o usuário está logado
        if login_required():
            return login_required()
            
        game = gamelist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))

        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return (redirect(url_for('cadgames')))
        return render_template('cadgames.html', gamelist=gamelist)

    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    # Definindo que o parâmetro é opcional
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        # print(res)
        data = res.read()
        gamesjson = json.loads(data)

        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'

        return render_template('apigames.html',
                               gamesjson=gamesjson)

    # ROTA COM O CRUD DE JOGOS
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            # Selecionando o jogo no banco para ser excluído
            game = Game.query.get(id)
            if game:
                # Deletar o game pelo ID
                db.session.delete(game)
                db.session.commit()
                flash('Jogo excluído com sucesso!', 'success')
            else:
                flash('Jogo não encontrado!', 'danger')
            return redirect(url_for('estoque'))

        if request.method == 'POST':
            # Cadastra um novo jogo
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'],
                           request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            # Envia os valores para o banco
            db.session.add(newgame)
            db.session.commit()
            flash('Jogo cadastrado com sucesso!', 'success')
            return redirect(url_for('estoque'))

        else:
            # PAGINAÇÃO
            # A variável abaixo captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 5)
            per_page = 5
            # Faz um SELECT no banco a partir da página informada (page)
            # Filtra os registros de 3 em 3 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', gamesestoque=games_page)

    # ROTA DE EDIÇÃO
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        # Buscando informações do jogo:
        game = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            game.titulo = request.form['titulo']
            game.ano = request.form['ano']
            game.categoria = request.form['categoria']
            game.plataforma = request.form['plataforma']
            game.preco = request.form['preco']
            game.quantidade = request.form['quantidade']
            db.session.commit()
            flash('Jogo atualizado com sucesso!', 'success')
            return redirect(url_for('estoque'))
        return render_template('editgame.html', game=game)

    # ROTA DE LOGIN
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = Usuario.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_email'] = user.email
                nickname = user.email.split('@')[0]
                flash(f'Login realizado com sucesso! Bem-vindo(a) {nickname}', 'success')
                return redirect(url_for('home'))
            else:
                flash('Email ou senha inválidos!', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html')

    # ROTA DE CADASTRO
    @app.route('/caduser', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            # Capturando os dados
            email = request.form['email']
            password = request.form['password']

            # Verificando se o usuário já existe
            user = Usuario.query.filter_by(email=email).first()
            # Se o usuário existir
            if user:
                msg = Markup("Usuário já cadastrado. Faça<a href='/login'>login.</a>")
                flash(msg, 'danger')
                return redirect(url_for('caduser'))
            # Caso o usuário não exista
            else:            
                # Gerando o hash
                hashed_password = generate_password_hash(password, method='scrypt')
                # Gravando no banco
                new_user = Usuario(email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                
                # Mensagem de sucesso após o cadastro
                flash('Registro realizado com sucesso! Faça o login', 'success')
                # Redirecionando para página de login
                return redirect(url_for('login'))
        return render_template('caduser.html')
