from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path
import json
from .config import load_config

PLAYERS_FILE = Path(__file__).resolve().parent.parent.parent / "players.json"

@dataclass
class Player:
    user_id: str
    xp: int = 0
    level: int = 1
    badges: List[str] = field(default_factory=list)
    streak: int = 0
    accuracy: float = 0.0
    region: str = "Global"

    def add_xp(self, amount: int):
        cfg = load_config()
        xp_per_level = cfg.get("gamification", {}).get("xp_per_level", 1000)
        self.xp += amount
        while self.xp >= self.level * xp_per_level:
            self.xp -= self.level * xp_per_level
            self.level += 1
            badge = f"Level_{self.level}"
            if badge not in self.badges:
                self.badges.append(badge)

class GamificationEngine:
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self._load()
        cfg = load_config().get("gamification", {})
        self.challenges = {
            "daily_threshold": {"xp": cfg.get("challenges", {}).get("daily_threshold", 150), "desc": "Flag any new CP ≥ 0.50"},
            "matrix_master": {"xp": cfg.get("challenges", {}).get("matrix_master", 400), "desc": "Analyze full multipolar matrix"},
            "rank_predictor": {"xp": cfg.get("challenges", {}).get("rank_predictor", 200), "desc": "Correctly predict rank change"},
            "first_flag": {"xp": cfg.get("challenges", {}).get("first_flag", 300), "desc": "First to flag new ongoing conflict"},
            "range_detector": {"xp": cfg.get("challenges", {}).get("range_detector", 250), "desc": "Detect high R_C cluster"},
        }

    def _load(self):
        if PLAYERS_FILE.exists():
            with open(PLAYERS_FILE, "r") as f:
                data = json.load(f)
            for uid, p in data.items():
                self.players[uid] = Player(**p)

    def _save(self):
        data = {uid: {
            "user_id": p.user_id, "xp": p.xp, "level": p.level,
            "badges": p.badges, "streak": p.streak, "accuracy": p.accuracy, "region": p.region
        } for uid, p in self.players.items()}
        with open(PLAYERS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def award(self, user_id: str, challenge_key: str, verified: bool = True):
        if not verified:
            return None
        player = self.players.setdefault(user_id, Player(user_id))
        reward = self.challenges.get(challenge_key, {"xp": 50})
        player.add_xp(reward["xp"])
        if challenge_key not in player.badges:
            player.badges.append(challenge_key)
        self._save()
        return {"user": user_id, "xp_gained": reward["xp"], "new_level": player.level, "badges": player.badges}

    def leaderboard(self, top_n: int = 10) -> List[Dict]:
        ranked = sorted(self.players.values(), key=lambda p: (p.level, p.xp), reverse=True)
        return [{"user": p.user_id, "level": p.level, "xp": p.xp, "badges": len(p.badges)} for p in ranked[:top_n]]
