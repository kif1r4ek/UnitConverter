import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.api.controller_pages import router as pages
from app.api.controller_length import router as length
from app.api.controller_temperature import router as temperature
from app.api.controller_weight import router as weight
from app.core.error_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.include_router(pages)
app.include_router(length)
app.include_router(temperature)
app.include_router(weight)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="0.0.0.0", port=8000)