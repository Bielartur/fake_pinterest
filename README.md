# Fake Pinterest

Projeto exemplo que simula parte das funcionalidades do Pinterest utilizando o framework **Flask**.

## Funcionalidades

- Cadastro de novos usuários com validações
- Login e logout de contas
- Upload de fotos para criar posts
- Feed público exibindo todas as fotos postadas
- Página de perfil para visualizar e remover próprias fotos
- Edição de perfil (nome, e-mail e foto de perfil)
- Senhas protegidas com *hash* (Bcrypt)
- Controle de sessão e proteção de rotas via Flask-Login
- Segurança adicional com Flask-Talisman (HTTPS e CSP)

## Tecnologias Utilizadas

- Python
- HTML
- CSS
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF / WTForms
- Flask-Talisman
- Gunicorn (produção)

Veja todas as dependências em [requirements.txt](requirements.txt).

## Como Executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Crie um arquivo `.env` definindo ao menos:

```
SECRET_KEY=<sua chave>
DEBUG=1           # ou 0 em produção
DATABASE_URL=<url do banco opcional>
```

3. Inicie a aplicação em modo de desenvolvimento:

```bash
python main.py
```

Acesse `http://localhost:5000` no navegador. Para produção use `gunicorn main:app` (ver `Procfile`).

## Estrutura do Projeto

```
fake_pinterest/
├── fakepinterest/
│   ├── __init__.py      # configuração do app Flask
│   ├── models.py        # modelos do banco
│   ├── forms.py         # formulários WTForms
│   ├── routes.py        # rotas da aplicação
│   ├── static/          # arquivos estáticos (CSS, JS, imagens)
│   └── templates/       # templates HTML
├── main.py              # ponto de entrada
└── requirements.txt
```

## Contribuindo

Contribuições são bem-vindas. Abra issues ou pull requests com melhorias.

