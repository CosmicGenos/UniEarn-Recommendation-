from typing import List
from fastapi import APIRouter, status
from fastapi.params import Depends
from datamodels.RequestDataModels import JobRequestData, StudentDetails
from datamodels.ResponseDataModels import  SearchResult
from services.RecommendationService import RecommendationService, get_recommendation_service

router = APIRouter(prefix='/recommendation', tags=['recommendation'])

@router.post('/save-jobs')
def save_jobs(job_details: List[JobRequestData],
              recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    try:
        results = recommendation_service.save_job(job_details)
        return {
            "status_code": 201,
            "success": True,
            "message": "Jobs saved successfully",
            "data": results
        }
    except Exception as e:
        return {
            "status_code": 500,
            "success": False,
            "message": "Failed to save jobs",
            "error": str(e)
        }

@router.post('/recommend-jobs')
def recommendation(student_details: StudentDetails,
                   recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    try:
        results = recommendation_service.recommend_jobs(student_details.text)
        return {
            "status_code": 200,
            "success": True,
            "message": "Recommendations retrieved successfully",
            "data": results
        }
    except Exception as e:
        return {
            "status_code": 500,
            "success": False,
            "message": "Failed to generate recommendations",
            "error": str(e)
        }

@router.put('/update-job')
def update_job(job_detail: JobRequestData,
               recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    try:
        result = recommendation_service.update_job(job_detail)
        return {
            "status_code": 200,
            "success": True,
            "message": f"Job {job_detail.jobID} updated successfully",
            "data": result
        }
    except Exception as e:
        return {
            "status_code": 500,
            "success": False,
            "message": f"Failed to update job {job_detail.jobID}",
            "error": str(e)
        }

@router.delete('/delete-job/{job_id}')
def delete_job(job_id: int,
               recommendation_service: RecommendationService = Depends(get_recommendation_service)):
    try:
        result = recommendation_service.delete_job(job_id)
        return {
            "status_code": 200,
            "success": True,
            "message": f"Job {job_id} deleted successfully",
            "data": {"deleted": result}
        }
    except Exception as e:
        return {
            "status_code": 500,
            "success": False,
            "message": f"Failed to delete job {job_id}",
            "error": str(e)
        }