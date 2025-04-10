from qdrant_client.http import models
from fastapi import Depends, HTTPException
from .QdrandDatabaseConnection import get_qdrant_connection, QdrantConnection


class QdrantCollectionManager:
    def __init__(self, qdrant_connection: QdrantConnection, vector_size: int = 384):
        self.vector_size = vector_size
        self.connection = qdrant_connection
        self.Collection_Structure = {
            "payload_fields": {
                "job_id": models.PayloadSchemaType.INTEGER,
                "title": models.PayloadSchemaType.KEYWORD,
                "category": models.PayloadSchemaType.KEYWORD,
                "status": models.PayloadSchemaType.KEYWORD,
                "start_at": models.PayloadSchemaType.DATETIME
            },
            "indexed_fields": ["status", "job_id"]
        }

    def create_collection_if_not_exists(self, collection_name: str = "jobs") -> None:
        try:
            client = self.connection.get_client()
            collections = client.get_collections()

            if collection_name not in [col.name for col in collections.collections]:
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    )
                )

                for field_name in self.Collection_Structure["indexed_fields"]:
                    field_type = self.Collection_Structure["payload_fields"][field_name]
                    client.create_payload_index(
                        collection_name=collection_name,
                        field_name=field_name,
                        field_schema=field_type
                    )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Collection creation failed: {str(e)}"
            )


def get_qdrant_collection_manager(
        qdrant_connection: QdrantConnection = Depends(get_qdrant_connection)
) -> QdrantCollectionManager:
    return QdrantCollectionManager(qdrant_connection)