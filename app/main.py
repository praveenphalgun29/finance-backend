from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, records, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="Backend API for a Finance Dashboard with role-based access control",
    version="1.0.0"
)

app.include_router(users.router, prefix="/auth", tags=["Auth & Users"])
app.include_router(records.router, prefix="/records", tags=["Financial Records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "Finance Dashboard API is running"}