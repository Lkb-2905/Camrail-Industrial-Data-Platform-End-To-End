import subprocess
import sys
import time
from loguru import logger

def main():
    logger.info("🚀 Démarrage de la Camrail Industrial Data Platform (Local)")
    
    try:
        # Lancer le consumer Kafka en arrière-plan
        logger.info("Démarrage du Thread Kafka Consumer...")
        kafka_process = subprocess.Popen([sys.executable, "src/kafka_consumer.py"])
        
        # Laisser le temps au consumer de s'initialiser
        time.sleep(2)
        
        # Lancer l'API Flask au premier plan
        logger.info("Démarrage de l'API Flask...")
        api_process = subprocess.Popen([sys.executable, "api/api.py"])
        
        # Garder le script principal actif
        kafka_process.wait()
        api_process.wait()
        
    except KeyboardInterrupt:
        logger.warning("🛑 Arrêt demandé par l'utilisateur. Fermeture des processus...")
        kafka_process.terminate()
        api_process.terminate()
        logger.success("Platforme arrêtée proprement.")

if __name__ == "__main__":
    main()
