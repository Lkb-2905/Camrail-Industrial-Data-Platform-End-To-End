import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, Response
from loguru import logger
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Ajout dynamique au PYTHONPATH (Gère l'import src depuis le parent dir)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config

# Stratégie de logging robuste
logger.add("logs/app.log", rotation="10 MB", retention="30 days")

# Sécurité & Environnement
load_dotenv()
API_PORT = int(os.getenv("API_PORT", 5000))
API_KEY = os.getenv("API_KEY", "entreprise_secret_key_2026")

# Schéma Entreprise (Pydantic Validation - Point 2)
class SensorEvent(BaseModel):
    loco_id: str
    flow_rate: float
    pressure: float
    vibration: float
    temperature: float

# Flask Serveur
app = Flask(__name__)

# Prometheus SRE Monitoring Metrics
PREDICTION_COUNT = Counter('api_predictions_total', 'Total number of predictions MLOps')
PREDICTION_LATENCY = Histogram('api_prediction_latency_seconds', 'Latency of Machine ML')
RISK_ALERT = Counter('api_risk_alerts_total', 'Total number of high risks anomalies')

# Chargement intelligent du Modèle IA via Registration (Models/)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, config['model']['registry_dir'], config['model']['latest_name'])

@app.route("/metrics", methods=["GET"])
def metrics() -> Response:
    """ SRE Scrape Endpoint metrics pour Prometheus """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/health", methods=["GET"])
def health() -> dict:
    """
    Healthcheck endpoint pour orchestrateurs DevOps type Kubernetes / Docker.
    
    Returns:
        tuple: (JSON Statut, Code HTTP 200)
    """
    return jsonify({"status": "ok", "service": "camrail-ml-api"}), 200

@app.route("/predict", methods=["POST"])
@PREDICTION_LATENCY.time()
def predict() -> dict:
    """
    Exposition du Moteur Random Forest IA de Maintenance Prédictive.
    
    Réceptionne : JSON contenant la télémétrie de la locomotive.
    Retourne : JSON détaillant la prédiction et probabilité MLOps (+ HTTP Statut).
    """
    # Point 6: Sécurité (API Key obligatoire)
    if request.headers.get("X-API-KEY") != API_KEY:
        logger.warning("Tentative d'accès non autorisé (API_KEY invalide ou manquante).")
        return jsonify({"error": "Unauthorized"}), 401
        
    try:
        data = request.get_json()
        
        # Point 2: Schema Validation (Pydantic)
        validated_data = SensorEvent(**data)
        data = validated_data.model_dump() if hasattr(validated_data, 'model_dump') else validated_data.dict()
        df_input = pd.DataFrame([data])
        
        if not os.path.exists(model_path):
            logger.error("Défaut de Model Registry : 'latest.pkl' manquant.")
            return jsonify({"error": "Modèle non entraîné. Déclenchez le DAG Airflow."}), 503
            
        model = joblib.load(model_path)
        
        # Sélection des colonnes MLOps
        features = df_input[['flow_rate', 'pressure', 'vibration', 'temperature']]
        
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0][1]
        
        PREDICTION_COUNT.inc()
        if int(prediction) == 1:
            RISK_ALERT.inc()
            
        logger.info(f"Requête entrante traitée - LocoID: {data.get('loco_id')} -> Proba de Panne: {proba:.2f}")
        
        return jsonify({
            "critical_risk": int(prediction),
            "risk_probability": round(float(proba), 4),
            "loco_id": validated_data.loco_id
        }), 200
        
    except ValidationError as ve:
        logger.error(f"Erreur de Schéma Pydantic: {ve}")
        return jsonify({"error": "Data Validation Failed", "details": ve.errors()}), 400
    except Exception as e:
        logger.error(f"Flask Worker Error: {e}")
        return jsonify({"error": str(e), "status": "Internal Error"}), 500

if __name__ == "__main__":
    logger.info(f"🚀 Déploiement du Serveur REST ({config['api']['host']}:{API_PORT})")
    app.run(host=config['api']['host'], port=API_PORT, debug=True)
