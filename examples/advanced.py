from typing import List, Any, Dict, Tuple

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi.openapi.utils
from pydantic import BaseModel

from fastapi_versionizer.versionizer import api_version, versionize

ICON_URL = 'https://avatars.githubusercontent.com/u/6480668?s=400&u=22411d8d949f102698c06b8c49b75f2a2827cb5e&v=4'


class TestModel(BaseModel):
    something: str


class ErrorResponseModel(BaseModel):
    code: str
    message: str


class ErrorResponsesModel(BaseModel):
    errors: List[ErrorResponseModel]


app = FastAPI(
    title='My Versioned API',
    description='Look, I can version my APIs!',
    version='2.0',
    responses={
        400: {'model': ErrorResponsesModel},
        500: {'model': ErrorResponsesModel}
    }
)


@app.post('/do_something', tags=['Something'], response_model=TestModel)
async def do_something(test: TestModel) -> Any:
    return test


@app.post('/do_something_else', tags=['Something Else'])
async def do_something_else() -> Any:
    return {'message': 'something else'}


@api_version(2)
@app.post('/do_something', tags=['Something'])
async def do_something_v2() -> Any:
    return {'message': 'something'}


@api_version(2)
@app.post('/do_something_new', tags=['Something New'])
async def do_something_new() -> Any:
    return {'message': 'something new'}


def get_openapi(app_: FastAPI, _: Tuple[int, int]) -> Dict[str, Any]:
    openapi_schema = fastapi.openapi.utils.get_openapi(
        title=app_.title,
        version=app_.version,
        routes=app_.routes
    )

    # Remove 422 response from schema
    for schema_path in openapi_schema['paths']:
        for method in openapi_schema['paths'][schema_path]:
            openapi_schema['paths'][schema_path][method]['responses'].pop('422', None)

    return openapi_schema


def get_docs(version: Tuple[int, int]) -> HTMLResponse:
    version_prefix = f'/v{version[0]}'
    return get_swagger_ui_html(
        openapi_url=f'{version_prefix}{app.openapi_url}',
        title=f'{app.title} - v{version[0]}',
        swagger_favicon_url=ICON_URL,
        swagger_ui_parameters={'defaultModelsExpandDepth': -1}
    )


def get_main_docs(_: List[Tuple[int, int]]) -> HTMLResponse:
    """
    This will expose a single, auto-generated "/versions" endpoint via a Swagger page.
    """

    return get_swagger_ui_html(
        openapi_url=f'{app.openapi_url}',
        title=f'{app.title}',
        swagger_favicon_url=ICON_URL,
        swagger_ui_parameters={'defaultModelsExpandDepth': -1}
    )


'''
- Create a main docs page at "/api_home", using the `get_main_docs` function
- Create "/v1/docs" and "/v2/docs" pages, because `docs_url` is given
- Note: This doesn't create redoc pages because `redoc_url` is not given
- Create a "latest" alias (and /docs page for it) using the "/" prefix

- This will create the following endpoints:
    - /api_home
    - /v1/docs
    - /v1/openapi.json
    - /v1/do_something
    - /v1/do_something_else
    - /v2/docs
    - /v2/openapi.json    
    - /v2/do_something
    - /v2/do_something_else
    - /v2/do_something_new
    - /docs
    - /openapi.json
    - /do_something
    - /do_something_else
    - /do_something_new
'''
versionize(
    app=app,
    prefix_format='/v{major}',
    main_docs_url='/api_home',
    get_openapi=get_openapi,
    get_main_docs=get_main_docs,
    get_docs=get_docs,
    docs_url='/specs',
    enable_latest=True,
    latest_prefix='/latest',
    swagger_ui_parameters={'defaultModelsExpandDepth': -1}
)
