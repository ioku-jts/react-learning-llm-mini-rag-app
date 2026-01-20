import os
import yaml
from openai import OpenAI

def load_openai_client():
    """
    Load OpenAI client from config.local.yaml or environment variable.
    """
    config_path = "config.local.yaml"

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return OpenAI(api_key=cfg["openai_api_key"])

    # Fallback to environment variable
    return OpenAI()
