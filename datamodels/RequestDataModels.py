from pydantic import BaseModel

class JobRequestData(BaseModel):
    jobID : int
    title: str
    jobDescription : str
    category: str
    status: str
    location : str
    finished_at : str
    salary :str
    company : str

class StudentDetails(BaseModel):
    text : str
