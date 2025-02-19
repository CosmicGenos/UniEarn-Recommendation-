from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from datamodels.RequestDataModels import JobRequestData, StudentDetails
from services.RecommendationService import RecommendationService,get_recommendation_service

router = APIRouter(prefix='/recommendation',tags=['recommendation'])

@router.post('/save-jobs')
def save_jobs(job_details:List[JobRequestData],
              recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    return recommendation_service.save_job(job_details)

@router.post('/recommend-jobs')
def recommendation (student_details:StudentDetails ,
                    recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    return recommendation_service.recommend_jobs(student_details.text)


