from typing import Any, Dict
import json
from .tokenizer import WWIATokenizer

def serialize_intelligence(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)

def tokenize_intelligence(data: Dict[str, Any], tokenizer: WWIATokenizer | None = None) -> Dict:
    if tokenizer is None:
        tokenizer = WWIATokenizer()
    text = serialize_intelligence(data)
    return {
        "raw_text": text,
        "token_count": tokenizer.count_tokens(text),
        "tokens": tokenizer.tokenize([text]),
    }
