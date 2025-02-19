from datetime import datetime
from typing import List, Dict, Any

from fastapi import HTTPException
from fastapi.params import Depends
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, PointStruct, UpdateResult


from databaseConnections.QdrandDatabaseConnection import QdrantConnection,get_qdrant_connection
from datamodels.ResponseDataModels import SearchResult


class JobRepository:

    def __init__(self,qclient: QdrantConnection,collection_name : str = 'jobs') :
        self.collection_name = collection_name
        self.qclient = qclient

    def store_job(self,job_embedding: List[float],job_payload: Dict[str,Any]) -> UpdateResult:
        try:
            client = self.qclient.get_client()
            result =   client.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(
                    id=job_payload["job_id"],
                    payload =job_payload,
                    vector = job_embedding
                )]
            )
            return result
        except Exception as e:
            raise HTTPException(status_code = 400,detail=f"Failed to create product: {str(e)}")

    def search_similar_jobs(
            self,
            query_embedding: List[float],
            status: str = "pending",
            # score_threshold: float = 0.5,
            limit = 200
    ) -> List[SearchResult]:
        try:
            client = self.qclient.get_client()
            status_filter = Filter(
                must=[
                    FieldCondition(
                        key="status",
                        match=MatchValue(value=status)
                    )
                ]
            )

            search_results = client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=status_filter,
                limit=limit,
                with_payload=True
            )

            sorted_results = sorted(search_results, key=lambda x: x.score, reverse=True)

            return [
                SearchResult(
                    job_id=point.payload['job_id'],
                    title=point.payload['title'],
                    category=point.payload['category'],
                    location=point.payload['location'],
                    salary=point.payload['salary'],
                    similarity_score=point.score
                )
                for point in sorted_results
            ]

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={"message": "Failed to search jobs", "error": str(e)}
            )

    async def update_job_completion_date(self,
            job_id: int,
            finished_at: datetime) -> UpdateResult:
        try:
            client = self.qclient.get_client()

            job_filter = Filter(
                must=[
                    FieldCondition(
                        key="job_id",
                        match=MatchValue(value=job_id)
                    )
                ]
            )

            search_results = client.scroll(
                collection_name=self.collection_name,
                query_filter=job_filter,
                limit=1,
                with_payload=True
            )

            points, _ = search_results
            if not points:
                raise HTTPException(status_code=404,detail=f"Job with ID {job_id} not found")

            point_id = points[0].id
            finished_at_iso = finished_at.isoformat()

            result = await client.set_payload(
                collection_name=self.collection_name,
                payload={
                    "finished_at": finished_at_iso,
                },
                points=[point_id],
                wait=True
            )

            if result.status != 'completed':
                raise HTTPException(status_code=500,detail="Update operation did not complete successfully")

            return result

        except Exception as e:
            raise HTTPException(status_code=500,detail={"message": f"Failed to update job {job_id}","error": str(e)})

    async def get_all_jobs( self) -> List[Dict[str, Any]]:

        try:
            client = self.qclient.get_client()

            points, _ = client.scroll(
                collection_name=self.collection_name,
                limit=100,
                with_payload=True,
                with_vector=False
            )

            job_payloads = [point.payload for point in points]
            return job_payloads

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Failed to retrieve jobs",
                    "error": str(e)
                }
            )


def get_job_repo(qclient: QdrantConnection = Depends(get_qdrant_connection)):
    return JobRepository(qclient)