from pydantic import BaseModel

class JobRequestData(BaseModel):
    jobID : int
    title: str
    jobDescription : str
    category: str
    status: str
    start_at : str
    company : str

class StudentDetails(BaseModel):
    text : str
