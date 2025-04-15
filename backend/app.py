from flask import Flask, jsonify, request
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from models import UserModel
import logging

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

# Conectar ao MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("URI do MongoDB não encontrada nas variáveis de ambiente")

client = MongoClient(MONGODB_URI)
db = client.get_database()  # Obtém o banco de dados da URI
users_collection = db["users"]  # Coleção de usuários
user_model = UserModel(users_collection)

@app.route('/')
def home():
    logger.info("Rota '/' acessada")
    return jsonify({"message": "Backend rodando!"})

@app.route('/api/register', methods=['POST'])
def register():
    logger.info("Tentativa de registro de novo usuário")
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Criar usuário
    result = user_model.create_user(name, email, password)
    if isinstance(result, dict) and "error" in result:
        logger.error(f"Erro no registro: {result['error']}")
        return jsonify(result), 400

    logger.info(f"Usuário registrado com sucesso: {result}")
    return jsonify({"message": "Usuário criado com sucesso!", "user_id": result}), 201

@app.route('/api/login', methods=['POST'])
def login():
    logger.info("Tentativa de login")
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        logger.error("Email e senha são obrigatórios")
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    # Verificar credenciais
    if not user_model.verify_password(email, password):
        logger.error("Credenciais inválidas")
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Gerar token JWT
    user = user_model.find_user_by_email(email)
    token = user_model.generate_token(str(user["_id"]))
    logger.info(f"Login bem-sucedido para o usuário: {user['_id']}")
    return jsonify({"message": "Login bem-sucedido!", "token": token}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)