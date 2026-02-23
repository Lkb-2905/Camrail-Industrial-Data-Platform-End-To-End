import json
import time
import os
import pandas as pd
from loguru import logger
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine
from pydantic import BaseModel, ValidationError
import os
import sys

# Ajout dynamique au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from dotenv import load_dotenv

load_dotenv()

logger.add("logs/kafka_consumer.log", rotation="10 MB", retention="30 days")

# Point 2 : Schema Validation stricte d'entreprise (Pydantic)
class SensorEvent(BaseModel):
    loco_id: str
    flow_rate: float
    pressure: float
    vibration: float
    temperature: float

def init_db_engine():
    db_user = os.getenv("POSTGRES_USER", "camrail_admin")
    db_pass = os.getenv("POSTGRES_PASSWORD", "enterprise_password_2026!")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "camrail_dwh")
    uri = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(uri)

def process_message(msg_value, engine):
    """ Valide le schéma et insère la donnée avec Retry Mechanism """
    try:
        data = json.loads(msg_value)
        # Validation Pydantic obligatoire
        validated_data = SensorEvent(**data)
        data = validated_data.model_dump() if hasattr(validated_data, 'model_dump') else validated_data.dict()
        df = pd.DataFrame([data])
        
        # Point 3 : Retry Mechanism de production
        for attempt in range(1, 4):
            try:
                df.to_sql("sensor_metrics", engine, if_exists="append", index=False)
                logger.info(f"💾 [CONSUMER] Insertion réussie loco: {validated_data.loco_id} (Essai {attempt})")
                return True
            except Exception as e:
                logger.warning(f"⚠️ [CONSUMER] Échec DB (Essai {attempt}/3): {e}")
                time.sleep(2 ** attempt)
                
        logger.error("🛑 [CONSUMER] Échec d'insertion définitif après 3 essais.")
        return False
        
    except ValidationError as ve:
        logger.error(f"❌ [CONSUMER] Rejet Pydantic Schema: {ve}")
    except json.JSONDecodeError as jse:
        logger.error(f"❌ [CONSUMER] Payload invalide: {jse}")
    return False

def run_consumer():
    kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
    topic = config['kafka']['topic']
    
    # Configuration Entreprise du Group ID
    conf = {
        'bootstrap.servers': kafka_broker,
        'group.id': 'dwh-etl-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    try:
        # Point 1 : Création stricte du Consumer
        consumer = Consumer(conf)
        consumer.subscribe([topic])
        engine = init_db_engine()
        
        logger.info(f"🚀 [CONSUMER] En écoute sur le topic Kafka: {topic}")

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"❌ [CONSUMER] Erreur Broker: {msg.error()}")
                    continue

            # Traitement sécurisé
            process_message(msg.value().decode('utf-8'), engine)

    except KeyboardInterrupt:
        logger.info("🛑 [CONSUMER] Arrêt manuel.")
    except Exception as e:
        logger.error(f"🔥 [CONSUMER] Crash fatal: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()

if __name__ == "__main__":
    run_consumer()
