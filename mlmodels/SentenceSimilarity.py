from typing import List
import torch
from sentence_transformers import SentenceTransformer

class TextEmbeddings:
    def __init__(self,model_name : str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.device = ('cuda' if torch.cuda.is_available() else 'cpu')

    def encode(self,text:str) -> List[float]:
        model = self.model.to(self.device)
        with torch.no_grad():
            embeddings = model.encode(text)
        return embeddings.tolist()

def get_embedding_model():
    return TextEmbeddings()


