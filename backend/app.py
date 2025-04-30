# Importações únicas e organizadas
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from middleware import token_required
from models import UserModel
from schemas import UserSchema
import os
import logging
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Configuração inicial
load_dotenv()

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inicialização do Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}})

# Conexão com MongoDB
try:
    MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(MONGODB_URI)
    db = client.aws_dashboard
    users_collection = db["users"]
    user_model = UserModel(users_collection)
    logger.info("Conexão ao MongoDB estabelecida com sucesso")
except Exception as e:
    logger.error(f"Erro ao conectar ao MongoDB: {e}")
    raise

# Configuração do Swagger
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Automação AWS API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Rotas

@app.route('/')
def home():
    """Rota Raiz
    ---
    get:
      summary: Verificar status da API
      responses:
        '200':
          description: API ativa
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    logger.info("Rota '/' acessada")
    return jsonify({"message": "Backend rodando!"})

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

    user = user_model.find_user_by_email(email)
    if not user or not user_model.verify_password(email, password):
        logger.error("Credenciais inválidas")
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = user_model.generate_token(str(user["_id"]))
    logger.info(f"Login bem-sucedido para o usuário: {user['_id']}")
    return jsonify({"message": "Login bem-sucedido!", "token": token}), 200

@app.route("/api/aws/credentials", methods=["POST"])
@token_required
def save_aws_credentials():
    """Salvar Credenciais AWS
    ---
    post:
      summary: Armazenar credenciais AWS temporariamente
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                accessKeyId:
                  type: string
                secretAccessKey:
                  type: string
              required:
                - accessKeyId
                - secretAccessKey
      responses:
        '200':
          description: Credenciais salvas com sucesso
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        '400':
          description: Credenciais ausentes
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
    """
    data = request.get_json()
    access_key = data.get("accessKeyId")
    secret_key = data.get("secretAccessKey")

    if not access_key or not secret_key:
        return jsonify({"error": "Credenciais AWS são obrigatórias"}), 400

    # Armazenar credenciais no MongoDB ou em um cache seguro (ex: Redis)
    return jsonify({"message": "Credenciais salvas temporariamente"}), 200

@app.route("/api/aws/lambda", methods=["GET"])
@token_required
def get_lambda_functions():
    """Listar Funções Lambda
    ---
    get:
      summary: Obter lista de funções Lambda do usuário
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Lista de funções retornada com sucesso
          content:
            application/json:
              schema:
                type: object
                properties:
                  functions:
                    type: array
                    items:
                      type: string
    """
    return jsonify({"functions": ["func1", "func2"]}), 200

@app.route('/api/protected', methods=['GET'])
@token_required
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
    return jsonify({"message": "Acesso concedido à rota protegida!"}), 200

# Executar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)