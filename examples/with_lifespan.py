# mypy: disable-error-code="no-any-return"
# flake8: noqa: A003

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter

from fastapi_versionizer.versionizer import Versionizer, api_version


class TestLifeSpan:
    initialized = False

    @classmethod
    def init(cls) -> None:
        cls.initialized = True


@asynccontextmanager
async def lifespan(_: FastAPI):
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
