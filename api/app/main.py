from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from logging.config import dictConfig
import logging
from log_config import LogConfig

from src.User import router as User
from src.Device import router as Device

from error import error_handler as eh
from error.NotFoundException import NotFoundException
from error.ValidationException import ValidationException


dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

tags_metadata = [
    {
        "name": "User",
        "description": "User related endpoints"
    },
    {
        "name": "Device",
        "description": "Device related endpoints"
    },
]

app = FastAPI(title="LleidaHack API",
              description="LleidaHack API",
              version="2.0",
              docs_url='/docs',
              redoc_url='/redoc',
              openapi_url='/openapi.json',
              openapi_tags=tags_metadata,
              debug=True,
              swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.add_exception_handler(NotFoundException, eh.not_found_exception_handler)
app.add_exception_handler(ValidationException, eh.validation_exception_handler)


# app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(User.router)
app.include_router(Device.router)


@app.get("/")
def root():
    return RedirectResponse(url='/docs')