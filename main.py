from fastapi import FastAPI
from app.core.config import get_settings
from app.api.endpoints import category, product, stock_movement# Se importa el router de las categorias

app = FastAPI(
    title="Management Inventory API",
    description="API for managing inventory, with product, category, stocks and users",
    version="0.1.0"
)

# Incluir router
app.include_router(category.router)
app.include_router(product.router)
app.include_router(stock_movement.router)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Management Inventory API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)