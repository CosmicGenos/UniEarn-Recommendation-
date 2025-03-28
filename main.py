from fastapi import FastAPI
from routers.RecomendationRouter import router

app = FastAPI()

app.include_router(router)
