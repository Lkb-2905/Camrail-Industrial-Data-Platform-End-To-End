import json
import time
import os
import pandas as pd
from loguru import logger
from confluent_kafka import Producer
from src.config import config
from dotenv import load_dotenv

load_dotenv()

# Logging rotation d'entreprise
logger.add("logs/kafka_producer.log", rotation="10 MB", retention="30 days")

def receipt(err, msg):
    if err is not None:
        logger.error(f"❌ [KAFKA] Erreur: {err}")
    else:
        logger.info(f"🚄 [KAFKA] Streaming Télémétrie envoyé sur le Topic: {msg.topic()} [Partition {msg.partition()}]")

def stream_telemetry():
    kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
    
    try:
        producer = Producer({'bootstrap.servers': kafka_broker})
    except Exception as e:
        logger.error("🛑 [KAFKA] Broker injoignable. Démarrez Docker Compose.")
        return

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sensors_path = os.path.join(base_dir, config['data']['raw_sensors'])
    
    try:
        df = pd.read_csv(sensors_path)
    except FileNotFoundError:
        logger.error("Défaut de data source pour le streaming.")
        return

    logger.info("📡 [STREAMING] Démarrage du Producteur IoT Kafka Azure vers DWH central...")
    
    for _, row in df.iterrows():
        data = row.to_dict()
        try:
            producer.produce(
                config['kafka']['topic'],
                key=str(data.get('loco_id', 'unknown')),
                value=json.dumps(data),
                callback=receipt
            )
            producer.poll(0)
            time.sleep(0.5) # Simule l'envoi IoT temps réel 500ms
        except Exception as buffer_error:
            logger.error(f"Buffer Kafka saturé: {buffer_error}")

    producer.flush()
    logger.info("✅ [STREAMING] Transmission Kafka Cloud achevée.")

if __name__ == "__main__":
    stream_telemetry()
