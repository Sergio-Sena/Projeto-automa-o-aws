<h1 align="center">🌐 AWS Services Dashboard</h1>

<p align="center">
  Painel com Flask + MongoDB + JWT para simular e integrar serviços AWS
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Flask-Backend-blue?logo=flask" />
  <img src="https://img.shields.io/badge/MongoDB-Database-brightgreen?logo=mongodb" />
  <img src="https://img.shields.io/badge/JWT-Auth-orange?logo=jsonwebtokens" />
  <img src="https://img.shields.io/badge/TailwindCSS-UI-blueviolet?logo=tailwindcss" />
  <img src="https://img.shields.io/badge/License-MIT-success" />
</p>

---

## 🧠 Sobre o Projeto

Este projeto é um painel interativo para **simular o acesso a serviços AWS** como Lambda, EC2 e DynamoDB.

- Backend em **Flask** com autenticação **JWT**
- Frontend com **TailwindCSS**
- Armazenamento de dados com **MongoDB**
- Endpoints simulados para prática de **integração e autenticação**
- Integração inicial com **Google Sign-In (em desenvolvimento)**

Ideal para estudos de integração com AWS, autenticação com JWT e criação de painéis administrativos em Python.

---

## 🧩 Estrutura do Projeto

```
aws-dashboard/
├── index.html
├── static/
│   └── js/
│       └── frontend.js
├── app.py
├── models.py
├── schemas.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Tecnologias Utilizadas

| Camada       | Tecnologia                                       |
|--------------|--------------------------------------------------|
| Frontend     | HTML5 + TailwindCSS + JavaScript puro           |
| Autenticação | JWT + Bearer Token                              |
| Banco de Dados | MongoDB Atlas / Local                        |
| Backend      | Flask (Python)                                  |
| Segurança    | Criptografia de senha com bcrypt                |
| Validação    | Marshmallow                                     |
| Documentação | Swagger UI integrado                            |
| CORS         | flask-cors                                      |

---

## ✅ Funcionalidades

- Registro de novos usuários no MongoDB
- Login com geração de token JWT
- Middleware de segurança com `@token_required`
- Envio de credenciais AWS para o backend
- Interface moderna com TailwindCSS
- Integração com Google Sign-In *(em progresso)*

---

## ⚙️ Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/aws-services-dashboard.git
cd aws-services-dashboard
```

### 2. Crie o ambiente virtual

#### Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure o `.env`

```env
MONGODB_URI=mongodb+srv://<usuario>:<senha>@cluster.mongodb.net/<banco>
JWT_SECRET=uma_chave_secreta_muito_segura_123!
```

### 4. Inicie o backend

```bash
python app.py
```

> O servidor estará disponível em: [http://localhost:5000](http://localhost:5000)

### 5. Inicie o frontend

Recomenda-se o uso da extensão **Live Server** no VS Code.

---

## 🌐 Endpoints Disponíveis

| Rota                     | Método | Descrição                         |
|--------------------------|--------|-----------------------------------|
| `/api/register`          | POST   | Registrar novo usuário            |
| `/api/login`             | POST   | Autenticação com JWT              |
| `/api/aws/credentials`   | POST   | Enviar credenciais AWS            |
| `/api/aws/lambda`        | GET    | Listar funções Lambda (fake)      |
| `/api/aws/ec2`           | GET    | Listar instâncias EC2             |
| `/api/aws/dynamodb`      | GET    | Listar tabelas DynamoDB           |
| `/swagger`               | GET    | Documentação Swagger              |

---

## 🧪 Exemplos de Uso (via Postman, curl, Thunder Client)

### Registro

```json
POST /api/register
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

### Login

```json
POST /api/login
{
  "email": "joao@example.com",
  "password": "senha123"
}
```

### Enviar Credenciais AWS

```http
POST /api/aws/credentials
Authorization: Bearer <token_jwt>
Content-Type: application/json

{
  "accessKeyId": "AKIA...",
  "secretAccessKey": "..."
}
```

---

## 🧠 Lógica do Frontend

- `handleLogin()` → chama `/api/login`  
- `handleSignup()` → chama `/api/register`  
- `handleAwsCredsSubmit()` → envia credenciais AWS  
- `showService()` → alterna entre os serviços  
- `localStorage.setItem("token")` → salva token JWT

---

## 📦 Requisitos do Backend

```txt
Flask==3.0.0
pymongo==4.6.0
PyJWT==2.8.0
bcrypt==4.1.0
flask-swagger-ui==0.0.1
marshmallow==3.20.1
flask-cors==4.0.0
python-dotenv==1.0.0
```

```bash
pip install -r requirements.txt
```

---

## 🔮 Futuras Melhorias

- [ ] Integração real com AWS SDK (boto3)  
- [ ] Refresh tokens com expiração automática  
- [ ] OAuth2 com Google Sign-In  
- [ ] Validação automática de credenciais AWS  
- [ ] Middleware JWT global

---

## 📬 Contribuição

Sinta-se à vontade para contribuir com PRs ou abrir *issues* com ideias como:

- Integração real com serviços AWS  
- Validação com AWS STS  
- Melhorias visuais no frontend  
- Adição de testes automatizados

---

## 📚 Licença

Distribuído sob a **MIT License**.  
Use livremente em projetos pessoais e comerciais.

---
