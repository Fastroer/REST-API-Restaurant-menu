from fastapi import FastAPI
from operations import router as router_operation

app = FastAPI()

app.include_router(router_operation)
