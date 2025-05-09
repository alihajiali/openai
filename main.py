from fastapi import Response, UploadFile, File, Depends, FastAPI, Depends, Request, APIRouter
from tortoise.contrib.fastapi import register_tortoise, RegisterTortoise
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
import asyncio, os, logging, uvicorn, json, time, subprocess, sys
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise, generate_config
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv
from utils import *
from src import *

TORTOISE_ORM = {
    'connections': {'main': os.getenv("SQL_URL")},
    'apps': {'app_main': {'models': ['main', 'aerich.models'],'default_connection': 'main'}}
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # asyncio.create_task(log_datetime())
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app = FastAPI(
    dependencies=[
        Depends(authorization)
    ], 
    lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

router = APIRouter(prefix=prefix)
router.include_router(chat_router)
app.include_router(router)

async def run_aerich_init():
    try:
        if "migrations" not in os.listdir():
            subprocess.run(["aerich", "init", "-t", "main.TORTOISE_ORM"], check=True)
            subprocess.run(["aerich", "init-db"], check=True)
        else:
            subprocess.run(["aerich", "migrate"])
            subprocess.run(["aerich", "upgrade"])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")    

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"{prefix}/", include_in_schema=False)
async def root():
    return f"APP IS RUNNING !"

@app.get(f"{prefix}/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url=f"{prefix}/openapi.json", title="docs")

@app.get(f"{prefix}/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url=f"{prefix}/openapi.json", title="docs")

@app.get(f"{prefix}/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    new_open_api_json = {}
    for path, value in get_openapi(title=app.title, version=app.version, routes=app.routes)["paths"].items():
        new_open_api_json[f"/{os.getenv('PREFIX')}{path}" if os.getenv('PREFIX') not in path else path]=value
    get_openapi(title=app.title, version=app.version, routes=app.routes)["paths"] = new_open_api_json
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        asyncio.run(run_aerich_init())
    else:
        uvicorn.run("main:app", host='0.0.0.0', port=int(os.getenv('PORT')), 
            log_level=logging.WARNING if os.getenv("RUNNING_MODE")=="deploy" else logging.INFO, 
            workers=2 if os.getenv("RUNNING_MODE")=="deploy" else 1, 
            reload=False if os.getenv("RUNNING_MODE")=="deploy" else True, 
        )