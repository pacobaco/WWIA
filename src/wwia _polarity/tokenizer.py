from transformers import AutoTokenizer
from typing import List, Dict

class WWIATokenizer:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_length = 512

    def tokenize(self, texts: List[str], return_tensors: str = "np") -> Dict:
        return self.tokenizer(
            texts, padding=True, truncation=True,
            max_length=self.max_length, return_tensors=return_tensors,
            return_attention_mask=True
        )

    def decode(self, input_ids) -> List[str]:
        return self.tokenizer.batch_decode(input_ids, skip_special_tokens=True)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text, add_special_tokens=True))
