from typing import List, Tuple, Dict, Any
from fastapi.params import Depends
from qdrant_client.http.models import UpdateResult

from databaseConnections.QdrantCollectionManager import QdrantCollectionManager,get_qdrant_collection_manager
from datamodels.RequestDataModels import JobRequestData
from datamodels.ResponseDataModels import SearchResult
from mlmodels.SentenceSimilarity import TextEmbeddings, get_embedding_model
from repositories.JobRepository import JobRepository, get_job_repo


class RecommendationService:

    def __init__(self,job_repo: JobRepository,
        collection_manager: QdrantCollectionManager,
        embedding_model: TextEmbeddings,expected_embed_size : int = 384):
        self.expected_embed_size = expected_embed_size
        self.job_repo = job_repo
        self.collection_manager = collection_manager
        self.embedding_model = embedding_model

    def job_preprocessing(self,request: JobRequestData) -> Tuple[str, Dict[str, Any]]:
        embedding_text = f"""Here is job Details
            Job Title: {request.title}
            Company: {request.company}
            Category: {request.category}
            Location: {request.location}
            Salary: {request.salary}
            Job Description: {request.jobDescription}
            """.strip()

        payload = {
            "job_id": request.jobID,
            "title": request.title,
            "category": request.category,
            "status": request.status,
            "location": request.location,
            "finished_at": request.finished_at,
            "salary": request.salary
        }

        return embedding_text, payload

    def save_job(self,job_details:List[JobRequestData])-> list[UpdateResult]:
        self.collection_manager.create_collection_if_not_exists()
        returnList = []
        for job_detail in job_details:
            job_embedding_text, job_payload = self.job_preprocessing(job_detail)
            job_embedding = self.embedding_model.encode(job_embedding_text)
            if len(job_embedding) != self.expected_embed_size:
                raise ValueError(f"Expected embedding size of 384, got {len(job_embedding)}")
            returnList.append(self.job_repo.store_job(job_embedding,job_payload))
        return returnList


    def recommend_jobs(self,student_details:str) -> List[SearchResult]:
        student_embedding = self.embedding_model.encode(student_details)
        if len(student_embedding) != self.expected_embed_size:
            raise ValueError(f"Expected embedding size of 384, got {len(student_embedding)}")
        return self.job_repo.search_similar_jobs(student_embedding)

def get_recommendation_service(
    job_repo: JobRepository = Depends(get_job_repo),
    collection_manager: QdrantCollectionManager = Depends(get_qdrant_collection_manager),
    embedding_model: TextEmbeddings = Depends(get_embedding_model)
) -> RecommendationService:
    return RecommendationService(
        job_repo=job_repo,
        collection_manager=collection_manager,
        embedding_model=embedding_model
    )










