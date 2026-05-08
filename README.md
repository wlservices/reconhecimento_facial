# Sistema de Reconhecimento Facial

Este projeto implementa um sistema de reconhecimento facial utilizando Python e o framework Flask. Ele é capaz de capturar streams de vídeo RTSP, processar as imagens para reconhecimento facial e gerenciar usuários com diferentes níveis de acesso (administrador, funcionário, supervisor).

## Funcionalidades

*   **Captura de Vídeo RTSP:** Integração com câmeras IP via protocolo RTSP para aquisição de frames.
*   **Reconhecimento Facial:** Processamento de imagens para identificar faces.
*   **Autenticação e Autorização:** Sistema de login com diferentes perfis de usuário (Admin, Employee, Supervisor) utilizando Flask-Login.
*   **Gerenciamento de Usuários:** Funcionalidades CRUD (Create, Read, Update, Delete) para usuários.
*   **Banco de Dados:** Utiliza SQLAlchemy para persistência de dados, com suporte a migrações via Flask-Migrate.

## Tecnologias Utilizadas

As principais tecnologias e bibliotecas utilizadas neste projeto incluem:

*   **Python 3.x**
*   **Flask:** Microframework web para Python.
*   **Flask-Login:** Gerenciamento de sessões de usuário.
*   **Flask-Migrate:** Extensão para lidar com migrações de banco de dados SQLAlchemy.
*   **python-dotenv:** Carrega variáveis de ambiente de um arquivo `.env`.
*   **OpenCV (cv2):** Biblioteca para visão computacional, utilizada no processamento de imagens.
*   **PyAV (av):** Biblioteca para manipulação de áudio e vídeo, utilizada para abrir streams RTSP.
*   **Werkzeug:** Biblioteca de utilitários para WSGI, usada para hashing de senhas.
*   **SQLAlchemy:** ORM (Object-Relational Mapper) para interação com o banco de dados.

## Estrutura do Projeto

A estrutura de diretórios do projeto é organizada da seguinte forma:

```
reconhecimento_facial/
├── migrations/             # Arquivos de migração do banco de dados
├── src/                    # Código-fonte da aplicação
│   ├── blueprints/         # Módulos da aplicação (admin, employee, supervisor)
│   │   ├── admin/          # Blueprint para funcionalidades administrativas
│   │   ├── employee/       # Blueprint para funcionalidades de funcionários
│   │   └── supervisor/     # Blueprint para funcionalidades de supervisores
│   ├── controller/         # Lógica de controle e manipulação de dados
│   ├── models/             # Definições dos modelos de dados (e.g., User)
│   │   ├── __init__.py
│   │   └── user.py         # Modelo de usuário com autenticação
│   ├── routes/             # Definição das rotas da aplicação
│   ├── static/             # Arquivos estáticos (CSS, JavaScript, imagens)
│   ├── templates/          # Templates HTML para as views
│   ├── decorator.py        # Decoradores personalizados
│   └── extensions.py       # Extensões do Flask (DB, LoginManager)
├── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore              # Arquivos e diretórios a serem ignorados pelo Git
├── main.py                 # Ponto de entrada principal da aplicação Flask
├── requirements.txt        # Lista de dependências do Python
└── rtsp_camera.py          # Script para captura e processamento de stream RTSP
```

## Instalação

Siga os passos abaixo para configurar e executar o projeto localmente:

### 1. Clonar o Repositório

```bash
git clone https://github.com/LuanCAlves/reconhecimento_facial.git
cd reconhecimento_facial
```

### 2. Criar e Ativar um Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate    # No Windows
```

### 3. Instalar Dependências

Instale todas as bibliotecas Python necessárias usando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```dotenv
DB_USER=seu_usuario_banco
DB_PASSWORD=sua_senha_banco
DB_ADDRESS=endereco_do_banco
DB_NAME=nome_do_banco
SECRET_KEY=uma_chave_secreta_forte
```

Se você estiver usando SQLite (padrão no `main.py` comentado), as variáveis de banco de dados não serão estritamente necessárias, mas `SECRET_KEY` é essencial para a segurança do Flask.

### 5. Inicializar o Banco de Dados

Execute as migrações para criar as tabelas no banco de dados:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Rodar a Aplicação

```bash
flask run
```

O aplicativo estará disponível em `http://127.0.0.1:5000/`.

## Uso

Após iniciar a aplicação, você pode acessar as diferentes funcionalidades através das rotas definidas. O sistema de reconhecimento facial (`rtsp_camera.py`) pode ser executado separadamente ou integrado à aplicação Flask, dependendo da arquitetura desejada.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório do GitHub.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (Assumindo que há um arquivo LICENSE no repositório, caso contrário, esta seção pode ser ajustada).
