import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from loguru import logger

def train_model(data_path, model_path):
    logger.info(f"🧠 Chargement des données pour entraînement : {data_path}")
    df = pd.read_csv(data_path)
    
    # Variables prédictives
    features = ['flow_rate', 'pressure', 'vibration', 'temperature', 'vibration_rolling_mean', 'pressure_rolling_mean']
    X = df[features]
    y = df['failure']
    
    logger.info("✂️  Séparation du jeu de données (Train: 80% / Test: 20%)")
    # Stratify assure qu'on a le même ratio de pannes dans l'entraînement et le test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    logger.info("🏗️  Entraînement de l'algorithme Random Forest (Optimisé pour les données déséquilibrées)...")
    # class_weight='balanced' est indispensable en maintenance où les pannes sont rares
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    rf_model.fit(X_train, y_train)
    
    logger.info("📊 Évaluation des performances du modèle :")
    y_pred = rf_model.predict(X_test)
    
    # Affichage du rapport de classification (Precision, Recall, F1-Score)
    report = classification_report(y_test, y_pred)
    logger.info(f"\n{report}")
    
    accuracy = accuracy_score(y_test, y_pred)
    logger.success(f"🏆 Précision globale (Accuracy) : {accuracy:.2%}")
    
    # Sauvegarde du modèle pour production
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(rf_model, model_path)
    logger.success(f"💾 Modèle sérialisé et sauvegardé pour la production : {model_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "processed_telemetry.csv")
    out_model = os.path.join(base_dir, "models", "rf_failure_predict.joblib")
    train_model(data_file, out_model)
