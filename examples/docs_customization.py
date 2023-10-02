# mypy: disable-error-code="no-any-return"
# flake8: noqa: A003

from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_redoc_html
import fastapi.openapi.utils
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Any, Tuple

from fastapi_versionizer.versionizer import Versionizer, api_version

ICON_URL = 'https://avatars.githubusercontent.com/u/6480668?s=400&u=22411d8d949f102698c06b8c49b75f2a2827cb5e&v=4'
USERNAME = 'test'
PASSWORD = 'secret!'

security = HTTPBasic()
app = FastAPI(
    title='test'
)


@api_version(1, 0)
@app.get('/status', tags=['Status'])
def get_status() -> str:
    return 'Ok - 1.0'


@api_version(1, 0, remove_in_major=2)
@app.get('/deps', tags=['Deps'])
def get_deps() -> str:
    return 'Ok'


@api_version(2, 0)
@app.get('/status', tags=['Status'])
def get_status_v2() -> str:
    return 'Ok - 2.0'


def callback(router: APIRouter, version: Tuple[int, int], version_prefix: str) -> None:
    title = f'test - {".".join(map(str, version))}' if version_prefix else 'test'

    @router.get('/openapi.json', include_in_schema=False)
    async def get_openapi() -> Any:
        openapi_schema = fastapi.openapi.utils.get_openapi(
            title=title,
            version=version_prefix[1:],
            routes=router.routes
        )

        # Change 200 response description
        for schema_path in openapi_schema['paths']:
            for method in openapi_schema['paths'][schema_path]:
                openapi_schema['paths'][schema_path][method]['responses']['200']['description'] = 'Success!'

        return openapi_schema

    @router.get('/docs', include_in_schema=False)
    async def get_docs(credentials: HTTPBasicCredentials = Depends(security)) -> Any:
        if credentials.username != USERNAME or credentials.password != PASSWORD:
            raise Exception('Invalid username/password')

        return get_swagger_ui_html(
            openapi_url=f'{version_prefix}/openapi.json',
            title=title,
            swagger_ui_parameters={
                'defaultModelsExpandDepth': -1
            },
            swagger_favicon_url=ICON_URL
        )

    @router.get('/redoc', include_in_schema=False)
    async def get_redoc(credentials: HTTPBasicCredentials = Depends(security)) -> HTMLResponse:
        if credentials.username != USERNAME or credentials.password != PASSWORD:
            raise Exception('Invalid username/password')

        return get_redoc_html(
            openapi_url=f'{version_prefix}/openapi.json',
            title=title,
            redoc_favicon_url=ICON_URL
        )


app, versions = Versionizer(
    app=app,
    prefix_format='/v{major}_{minor}',
    semantic_version_format='{major}.{minor}',
    latest_prefix='/latest',
    sort_routes=True,
    include_main_docs=False,
    include_version_docs=False,
    include_version_openapi_route=False,
    include_main_openapi_route=False,
    callback=callback
).versionize()


# Add main docs pages, with all versioned routes
callback(app.router, (2, 0), '')
