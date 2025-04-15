import jwt
from flask import request, jsonify
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verificar se o token está presente no cabeçalho da requisição
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token ausente"}), 401

        try:
            # Decodificar o token
            secret_key = "seu_segredo_jwt"  # Substitua por sua chave secreta
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user_id = data["user_id"]
        except Exception as e:
            return jsonify({"error": "Token inválido", "details": str(e)}), 401

        # Passar o ID do usuário para a função decorada
        kwargs["current_user_id"] = current_user_id
        return f(*args, **kwargs)

    return decorated