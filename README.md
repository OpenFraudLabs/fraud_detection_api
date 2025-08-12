                                                FRAUD DETECTION DEPLOYABLE API

<img width="1472" height="1602" alt="deepseek_mermaid_20250812_e40e4f" src="https://github.com/user-attachments/assets/444d3f93-a108-4253-8072-46f29104a186" />

A RESTful API for detecting fraudulent transactions using machine learning. Deployable via Docker or locally with FastAPI.

-----------

📌KEY FEATURES

Real-time fraud prediction (JSON input/output)

Pre-trained ML model integrated via FastAPI

Docker support for containerized deployment

Swagger UI auto-documentation at /docs

-------------------

🛠️ INSTALLATION

Option 1: Local Setup bash

git clone https://github.com/OpenFraudLabs/fraud_detection_api.git

cd fraud-detection-api

pip install -r requirements.txt

uvicorn main:app --reload

Option 2: Docker bash

docker build -t fraud-api .

docker run -p 8000:8000 fraud-api

-----

SYSTEM ARCHITECHURE 

<img width="2972" height="351" alt="deepseek_mermaid_20250812_303d13" src="https://github.com/user-attachments/assets/b4c1c553-e664-4991-be8f-c71e3632fe37" />

---------------
🚀 USAGE

Sample Request bash

curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{"amount": 150.0, "merchant": "M123", "user_id": "U456"}'

Sample Response

json
{
  "is_fraud": true,
  
  "confidence": 0.97  
}

------

📜 API REFRENCE 

Endpoint	Method	Description

/predict	POST	Submit transaction for analysis

/docs	GET	Interactive API documentation

------

🤝CONTRIBUTING

Fork the repository

Create a feature branch (git checkout -b feature/your-feature)

Submit a PR with tests 

----------------
📄 License

MIT © OpenFraudLabs
