from typing import List, Dict
import json
from pathlib import Path

SAMPLE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "sample_posts.json"

def load_sample_posts(country: str | None = None) -> List[Dict]:
    if not SAMPLE_PATH.exists():
        return _synthetic(country)
    with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if country:
        return [p for p in data if p.get("country", "").upper() == country.upper()]
    return data

def collect_posts(country: str, limit: int = 2000) -> List[Dict]:
    posts = load_sample_posts(country)
    return posts[:limit]

def _synthetic(country: str | None) -> List[Dict]:
    base = [
        {"text": "Strong national security and borders for Israel.", "engagement": 180, "country": "IL"},
        {"text": "Iranian proxies and Hormuz threats must end.", "engagement": 210, "country": "US"},
        {"text": "Resistance continues against aggression in the strait.", "engagement": 160, "country": "IR"},
        {"text": "Houthi attacks serve Iranian project against Saudi.", "engagement": 190, "country": "SA"},
        {"text": "Yemeni forces standing with Iran against blockade.", "engagement": 140, "country": "YE"},
        {"text": "Ukraine will never surrender to Russian aggression.", "engagement": 220, "country": "UA"},
        {"text": "Special military operation ongoing successfully.", "engagement": 170, "country": "RU"},
        {"text": "America stands with allies while securing Hormuz.", "engagement": 200, "country": "US"},
        {"text": "New regional defense understanding with partners.", "engagement": 130, "country": "TR"},
        {"text": "Pakistan engages constructively with regional neighbors.", "engagement": 110, "country": "PK"},
        {"text": "Taiwan strengthens drone defenses drawing Ukraine lessons.", "engagement": 150, "country": "TW"},
        {"text": "China pursues peaceful reunification and multipolar order.", "engagement": 140, "country": "CN"},
    ]
    if country:
        return [p for p in base if p["country"].upper() == country.upper()]
    return base
