from pathlib import Path
import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent.parent / "config.yaml"

def load_config(path: str | Path = DEFAULT_CONFIG) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
