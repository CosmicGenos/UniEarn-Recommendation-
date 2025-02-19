from sqlmodel import create_engine, Session
from functools import lru_cache
from redis import Redis
from qdrant_client import QdrantClient


class PostgresConnection:

    def __init__(self, host="localhost", port=5432, user="root",
                 password="1234", database="fastapidb", echo=True):
        self.psql_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.psql_engine = create_engine(self.psql_url, echo=echo)

    def get_session(self):
        with Session(self.psql_engine) as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

    def dispose(self):
        self.psql_engine.dispose()




class RedisConnection:
    def __init__(self, host="localhost", port=6379, db=0,
                 socket_timeout=5, decode_responses=True):
        self.client = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
            socket_timeout=socket_timeout
        )

    def get_client(self):
        try:
            self.client.ping()
            return self.client
        except Exception as e:
            raise ConnectionError(f"Redis connection failed: {str(e)}")

    def close(self):
        self.client.close()



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
def get_postgres_connection():
    return PostgresConnection()


@lru_cache()
def get_redis_connection():
    return RedisConnection()


@lru_cache()
def get_qdrant_connection():
    return QdrantConnection()