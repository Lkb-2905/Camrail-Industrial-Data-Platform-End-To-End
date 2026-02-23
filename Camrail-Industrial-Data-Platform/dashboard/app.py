import streamlit as st
import pandas as pd
import requests
import json
import sys
import os

# Gestion dynamique du répertoire racine et config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import config

st.set_page_config(page_title="Camrail Live Monitor", layout="wide", page_icon="🚂")

st.title("🏭 Camrail Industrial Data Platform")
st.markdown("**(Production V2 Level-CAC40)** - *Monitoring en Temps Réel et Maintenance AI*")

# Mode démo manuelle 
st.sidebar.header("🔬 Outil de Test Manuel (API)")
loco_id = st.sidebar.text_input("Identifiant Locomotive", value=config['dashboard']['mock_loco_id'])
flow_rate = st.sidebar.slider("Débit d'Huile (L/min)", 200, 800, 500)
pressure = st.sidebar.slider("Pression (Bar)", 1.0, 10.0, 5.0)
vibration = st.sidebar.slider("Vibrations (mm/s)", 0.5, 15.0, 2.0)
temperature = st.sidebar.slider("Température (°C)", 20.0, 120.0, 45.0)

if st.sidebar.button("⚙️ Interroger l'API Neural Network"):
    # Requête HTTP vers le serveur backend qui écoute sur 5000 (Désigné dans .env)
    url = f"http://{config['api']['host']}:5000/predict"
    payload = {
        "loco_id": loco_id,
        "flow_rate": flow_rate,
        "pressure": pressure,
        "vibration": vibration,
        "temperature": temperature
    }
    
    api_key = os.getenv("API_KEY", "entreprise_secret_key_2026")
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    with st.spinner("Analyse Cloud MLOps en cours..."):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                res = response.json()
                risk = res.get("critical_risk", 0)
                proba = res.get("risk_probability", 0.0)
                
                if risk == 1:
                    st.error(f"🚨 ALERT : DANGER DÉTECTÉ POUR **{loco_id}**. (Signatures Métriques Alarmantes)")
                    st.toast(f"Taux de Fiabilité Machine: {(1.0-proba)*100:.1f}%", icon="💥")
                else:
                    st.success(f"✅ OPÉRATION NOMINALE POUR **{loco_id}**.")
                    st.toast(f"Taux de Fiabilité Machine: {(1.0-proba)*100:.1f}%", icon="✔️")
            else:
                st.warning(f"⚠️ Erreur Applicative Server Node : {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ API injoignable. Vérifiez que l'API Flask tourne : `python api/api.py`")
        except requests.exceptions.ReadTimeout:
            st.error("❌ Timeout API. L'API met trop de temps à répondre. Vérifiez qu'elle tourne et réessayez.")

st.markdown("---")
st.markdown("### 📊 Architecture Cloud CI/CD et Modulaire")
st.write("Couplage API REST Dockerisée / Modèle stocké dans un Registry MLOps (`latest.joblib`). Déploiement Azure / AWS ready.")
st.button("Actualiser la page", type="secondary")
