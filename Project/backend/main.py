from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.benchmark import router as benchmark_router


app = FastAPI(
    version="1.0.0",
    title="Data Framework Benchmark API",
    description="API for comparing dataclasses, Pydantic, and msgspec performance",
)

app.add_middleware(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    middleware_class=CORSMiddleware,
)

@app.get(path="/health")
async def health_check() -> dict:
    return {"status": "healthy"}

app.include_router(router=benchmark_router, prefix="/api")

if __name__ == "__main__":
    import os
    import uvicorn

    port = 8000
    host = "0.0.0.0"
    # host = "0.0.0.0" if os.getenv("DOCKER_ENV") else "127.0.0.1"
    
    uvicorn.run(
        app="main:app", 
        host=host, 
        port=port, 
        reload=True,
        log_level="info"
    )
