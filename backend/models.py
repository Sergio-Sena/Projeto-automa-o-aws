from pymongo.collection import Collection
from bson.objectid import ObjectId
import bcrypt
import jwt
from datetime import datetime, timedelta
from marshmallow import ValidationError
from schemas import UserSchema
from config import Config  # Importa configurações centralizadas

class UserModel:
    def __init__(self, collection: Collection):
        self.collection = collection
        self.secret_key = Config.JWT_SECRET  # Chave segura do `.env`

    def validate_data(self, data: dict) -> bool | dict:
        """
        Valida os dados de entrada com o esquema definido.
        Retorna True se válido ou um dicionário de erros.
        """
        try:
            UserSchema().load(data)
            return True
        except ValidationError as err:
            return {"error": err.messages}

    def create_user(self, name: str, email: str, password: str) -> str | dict:
        """
        Cria um novo usuário após validar os dados e verificar duplicidade.
        """
        validation_result = self.validate_data({"name": name, "email": email, "password": password})
        if isinstance(validation_result, dict):
            return validation_result

        if self.find_user_by_email(email):
            return {"error": "Email já cadastrado"}

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def find_user_by_email(self, email: str) -> dict | None:
        """
        Busca um usuário pelo email.
        """
        user = self.collection.find_one({"email": email})
        return user  # Retorna None se não encontrado

    def find_user_by_id(self, user_id: str) -> dict | None:
        """
        Busca um usuário pelo ID interno do MongoDB.
        """
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            return user
        except Exception:
            return {"error": "ID inválido"}

    def verify_password(self, email: str, password: str) -> bool | dict:
        """
        Verifica se a senha fornecida corresponde à do usuário.
        """
        user = self.find_user_by_email(email)
        if not user:
            return {"error": "Usuário não encontrado"}
        return bcrypt.checkpw(password.encode("utf-8"), user["password"])

    def generate_token(self, user_id: str) -> str:
        """
        Gera um token JWT com expiração de 1 hora.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")