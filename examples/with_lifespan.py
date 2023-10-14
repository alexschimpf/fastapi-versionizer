# mypy: disable-error-code="no-any-return"
# flake8: noqa: A003

from contextlib import asynccontextmanager
import time
from typing import AsyncGenerator, Awaitable, Callable
from fastapi import FastAPI, APIRouter, Request, Response

from fastapi_versionizer.versionizer import Versionizer, api_version


class TestLifeSpan:
    initialized = False

    @classmethod
    def init(cls) -> None:
        cls.initialized = True


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    try:
        TestLifeSpan.init()
        yield
    finally:
        pass


app = FastAPI(
    title='test',
    docs_url='/swagger',
    openapi_url='/api_schema.json',
    redoc_url=None,
    lifespan=lifespan
)
status_router = APIRouter(
    prefix='/status',
    tags=['Status']
)

@app.middleware('http')
async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

@api_version(1)
@status_router.get('', deprecated=True)
def get_v1_status() -> str:
    if not TestLifeSpan.initialized:
        raise Exception('Lifespan not initialized')
    return 'Ok'


@api_version(2)
@status_router.get('')
def get_v2_status() -> str:
    if not TestLifeSpan.initialized:
        raise Exception('Lifespan not initialized')
    return 'Ok'


app.include_router(status_router)

app, versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    include_versions_route=True,
    sort_routes=True
).versionize()
