from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends
from app.config.database import init_db
from app.routes.tasks import router as task_router
from app.routes.auth_routes import router as auth_router
from app.middleware.auth import JWTBearer
@asynccontextmanager
async def lifespan(ap:FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(task_router,prefix="/api",tags=['Tasks'])
# app.include_router(task_router,prefix="/api",tags=['Tasks'])
app.include_router(auth_router,prefix="/api/auth",tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}

