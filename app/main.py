import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.controllers.pages.controller_pages import router as pages
from app.controllers.length.controller_length import router as length
from app.controllers.temperature.controller_temperature import router as temperature
from app.controllers.weight.controller_weight import router as weight

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.include_router(pages)
app.include_router(length)
app.include_router(temperature)
app.include_router(weight)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="0.0.0.0", port=8000)