# Blog de Notícias com Flask e MySQL

Um sistema de blog de notícias desenvolvido com Flask, MySQL e SQLAlchemy, incluindo funcionalidades de autenticação, gerenciamento de notícias, galeria de imagens, comentários e sistema de curtidas.

## Funcionalidades

- **Autenticação de Usuários**
  - Login/Logout
  - Primeiro usuário cadastrado automaticamente se torna administrador
  - Área restrita para administradores
  - Proteção de rotas com @login_required

- **Gerenciamento de Notícias**
  - Criar, editar e excluir notícias (apenas administradores)
  - Upload de imagens para notícias
  - Visualização de notícias com imagens
  - Listagem de notícias com paginação
  - Sistema de curtidas em notícias

- **Galeria de Imagens**
  - Upload de imagens (apenas administradores)
  - Vinculação de imagens a notícias
  - Visualização de galeria por notícia
  - Exclusão de imagens
  - Geração automática de nomes únicos para imagens

- **Sistema de Comentários**
  - Comentários em notícias
  - Exclusão de comentários (apenas administradores e autores)
  - Formatação de data e hora
  - Validação de conteúdo

- **Sistema de Curtidas**
  - Curtir/Descurtir notícias
  - Contagem de curtidas em tempo real
  - Interface intuitiva com ícones
  - Restrição para usuários logados

- **Interface Moderna**
  - Design responsivo com Bootstrap 5
  - Ícones do Font Awesome
  - Mensagens flash elegantes com animações
  - Navegação intuitiva
  - Feedback visual para ações do usuário

## Requisitos

- Python 3.7+
- MySQL Server
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/marcelitos1v9/blog_flask_mysql
cd blog_flask_mysql
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Certifique-se que o MySQL está instalado e rodando:
- Instale o MySQL Server se ainda não tiver
- O sistema está configurado para usar:
  - Host: localhost
  - Usuário: root
  - Senha: (vazia)
  - Banco de dados: blog_news

## Configuração

O sistema está configurado para funcionar sem arquivo `.env`. As configurações estão definidas no arquivo `config/database.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blog_news',
    'charset': 'utf8mb4'
}
```

Se necessário, você pode alterar estas configurações editando o arquivo `config/database.py`.

## Primeiro Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse o sistema:
- Abra seu navegador e acesse: `http://localhost:4000`

3. Crie seu primeiro usuário:
- Clique em "Registrar" na página inicial
- Preencha os dados do usuário
- O primeiro usuário cadastrado será automaticamente definido como administrador

4. Faça login com seu usuário:
- Use as credenciais criadas no passo anterior
- Como administrador, você terá acesso a todas as funcionalidades do sistema

## Funcionalidades do Administrador

Como administrador, você terá acesso a:

- Criar, editar e excluir notícias
- Upload de imagens para a galeria
- Gerenciar comentários
- Acesso ao painel administrativo
- Exclusão de imagens da galeria

## Estrutura do Projeto

```
blog_flask_mysql/
├── app.py                  # Arquivo principal da aplicação
├── requirements.txt        # Dependências do projeto
├── config/                 # Configurações do sistema
│   └── database.py        # Configurações do banco de dados
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   └── uploads/           # Pasta para uploads de imagens
├── models/                 # Modelos do banco de dados
│   ├── user.py           # Modelo de usuário
│   ├── news.py           # Modelo de notícias
│   ├── gallery.py        # Modelo da galeria
│   ├── comment.py        # Modelo de comentários
│   └── like.py           # Modelo de curtidas
└── views/                 # Rotas e templates
    ├── auth.py           # Rotas de autenticação
    ├── news.py           # Rotas de notícias
    ├── gallery.py        # Rotas da galeria
    ├── comments.py       # Rotas de comentários
    ├── likes.py          # Rotas de curtidas
    └── templates/        # Templates HTML
```

## Segurança

- O sistema utiliza Flask-Login para autenticação
- Senhas são armazenadas com hash seguro
- Acesso restrito para funções administrativas
- Proteção contra CSRF
- Validação de uploads de arquivos
- Sanitização de inputs
- Proteção contra SQL Injection
- Validação de tipos de arquivo permitidos

## Suporte

Se encontrar algum problema ou tiver dúvidas, abra uma issue no repositório do projeto.

