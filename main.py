from fastapi import fastapi

app = FastAPI(
    title="Management Inventory API",
    description="API for managing inventory, with product, category, stocks and users",
    version="0.1.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Management Inventory API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)