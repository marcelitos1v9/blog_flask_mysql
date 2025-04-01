# Blog de Notícias

Um sistema web para gerenciamento de notícias e galeria de imagens, desenvolvido com Flask e MySQL.

## Funcionalidades

- Cadastro e autenticação de usuários
- Controle de acesso (admin/usuário comum)
- Criação, edição e exclusão de notícias
- Upload e gerenciamento de imagens na galeria
- Interface responsiva com Bootstrap

## Requisitos

- Python 3.8 ou superior
- MySQL 5.7 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/blog-noticias.git
cd blog-noticias
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
- Crie um banco de dados MySQL chamado `blog_news`
- Configure as credenciais do banco no arquivo `.env`:
```
DATABASE_URL=mysql://usuario:senha@localhost/blog_news
SECRET_KEY=sua-chave-secreta-aqui
```

5. Inicialize o banco de dados:
```bash
python app.py
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse a aplicação no navegador:
```
http://localhost:4000
```

3. Crie um usuário administrador:
- Acesse a página de registro
- Crie uma conta
- No banco de dados, defina `is_admin = True` para o usuário criado

## Estrutura do Projeto

```
blog-noticias/
├── app.py              # Arquivo principal da aplicação
├── models/             # Modelos do banco de dados
│   ├── user.py
│   ├── news.py
│   └── gallery.py
├── views/              # Blueprints e templates
│   ├── auth.py
│   ├── news.py
│   ├── gallery.py
│   └── templates/
├── static/             # Arquivos estáticos
│   ├── css/
│   └── uploads/
└── requirements.txt    # Dependências do projeto
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 