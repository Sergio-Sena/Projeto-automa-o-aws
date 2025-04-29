from flask import Flask, jsonify, request
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from models import UserModel
import logging
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Configurar logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Salvar logs em um arquivo
        logging.StreamHandler()         # Exibir logs no terminal
    ]
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
     r"/*": {"origins": "http://localhost:5500/frontend/index.html"}})

# Conectar ao MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("URI do MongoDB não encontrada nas variáveis de ambiente")

client = MongoClient(MONGODB_URI)
db = client.get_database()  # Obtém o banco de dados da URI
users_collection = db["users"]  # Coleção de usuários
user_model = UserModel(users_collection)

# Configuração do Swagger
SWAGGER_URL = "/swagger"  # URL onde o Swagger será acessado
API_URL = "/static/swagger.json"  # Localização do arquivo JSON da API

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Automação AWS API"}  # Nome exibido no Swagger UI
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Rota inicial


@app.route('/')
def home():
    logger.info("Rota '/' acessada")
    return jsonify({"message": "Backend rodando!"})

# Rota de registro


@app.route('/api/register', methods=['POST'])
def register():
    """Registro de Usuário
    ---
    post:
      summary: Registrar um novo usuário
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
              required:
                - name
                - email
                - password
      responses:
        '201':
          description: Usuário criado com sucesso
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  user_id:
                    type: string
        '400':
          description: Erro de validação ou email já cadastrado
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    logger.info("Tentativa de registro de novo usuário")
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    result = user_model.create_user(name, email, password)
    if isinstance(result, dict) and "error" in result:
        logger.error(f"Erro no registro: {result['error']}")
        return jsonify(result), 400

    logger.info(f"Usuário registrado com sucesso: {result}")
    return jsonify({"message": "Usuário criado com sucesso!", "user_id": result}), 201

# Rota de login


@app.route('/api/login', methods=['POST'])
def login():
    """Login de Usuário
    ---
    post:
      summary: Autenticar um usuário
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
              required:
                - email
                - password
      responses:
        '200':
          description: Login bem-sucedido
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  token:
                    type: string
        '400':
          description: Email ou senha ausentes
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
        '401':
          description: Credenciais inválidas
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    logger.info("Tentativa de login")
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        logger.error("Email e senha são obrigatórios")
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    if not user_model.verify_password(email, password):
        logger.error("Credenciais inválidas")
        return jsonify({"error": "Credenciais inválidas"}), 401

    user = user_model.find_user_by_email(email)
    token = user_model.generate_token(str(user["_id"]))
    logger.info(f"Login bem-sucedido para o usuário: {user['_id']}")
    return jsonify({"message": "Login bem-sucedido!", "token": token}), 200

# Rota protegida (exemplo)


@app.route('/api/protected', methods=['GET'])
def protected_route():
    """Rota Protegida
    ---
    get:
      summary: Acessar uma rota protegida
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Acesso concedido
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        '401':
          description: Token ausente ou inválido
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    return jsonify({"message": "Esta é uma rota protegida!"}), 200


# Executar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
