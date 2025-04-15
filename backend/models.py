from pymongo.collection import Collection
from bson.objectid import ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from schemas import UserSchema, validate_data

# Modelo de Usuário
class UserModel:
    def __init__(self, collection: Collection):
        self.collection = collection
        self.secret_key = "seu_segredo_jwt"  # Substitua por uma chave segura

    # Função para validar dados
    def validate_data(self, data):
        try:
            UserSchema().load(data)
            return True
        except ValidationError as err:
            return {"error": err.messages}

    # Criar usuário
    def create_user(self, name: str, email: str, password: str):
        # Validar dados antes de salvar
        validation_result = self.validate_data({"name": name, "email": email, "password": password})
        if isinstance(validation_result, dict):  # Se houver erros de validação
            return validation_result

        # Verificar se o usuário já existe
        existing_user = self.find_user_by_email(email)
        if existing_user:
            return {"error": "Email já cadastrado"}

        # Criptografar a senha com bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,  # Senha criptografada
            "createdAt": datetime.now()
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    # Encontrar usuário por email
    def find_user_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    # Encontrar usuário por ID
    def find_user_by_id(self, user_id: str):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    # Verificar senha
    def verify_password(self, email: str, password: str):
        user = self.find_user_by_email(email)
        if not user:
            return False
        # Verificar se a senha fornecida corresponde à senha criptografada
        return bcrypt.checkpw(password.encode("utf-8"), user["password"])

    # Gerar token JWT
    def generate_token(self, user_id: str):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token expira em 1 hora
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")