import yaml
import os

def load_config():
    """
    Charge la configuration centralisée depuis le fichier config.yaml.
    
    Returns:
        dict: Dictionnaire contenant la configuration de l'application.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "config.yaml")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    return config

config = load_config()
