from functools import lru_cache
from qdrant_client import QdrantClient


class QdrantConnection:
    def __init__(self, host="localhost", port=6333, timeout=10):
        self.client = QdrantClient(
            host=host,
            port=port,
            timeout=timeout
        )

    def get_client(self):
        try:
            self.client.get_collections()
            return self.client
        except Exception as e:
            raise ConnectionError(f"Qdrant connection failed: {str(e)}")

    def close(self):
        self.client.close()

@lru_cache()
def get_qdrant_connection():
    return QdrantConnection()