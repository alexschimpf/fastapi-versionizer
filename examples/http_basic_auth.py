from typing import Any, Tuple
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from pydantic import BaseModel

from fastapi_versionizer.versionizer import api_version, versionize


USERNAME = 'test'
PASSWORD = 'secret!'

security = HTTPBasic()
app = FastAPI(
    title='My Versioned API',
    description='Look, I can version my APIs!'
)


class TestModel(BaseModel):
    something: str


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


def callback(app_: FastAPI, _: Tuple[int, int], prefix: str) -> None:
    title = f'{app_.title} - {prefix}'
    openapi_url = f'{prefix}{app_.openapi_url}'

    @app_.get('/docs', include_in_schema=False)
    def get_docs(credentials: HTTPBasicCredentials = Depends(security)) -> HTMLResponse:
        if credentials.username != USERNAME or credentials.password != PASSWORD:
            raise Exception('Invalid username/password')

        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=title
        )

    @app_.get('/redoc', include_in_schema=False)
    def get_redoc(credentials: HTTPBasicCredentials = Depends(security)) -> HTMLResponse:
        if credentials.username != USERNAME or credentials.password != PASSWORD:
            raise Exception('Invalid username/password')

        return get_redoc_html(
            openapi_url=openapi_url,
            title=title
        )


'''
We call `versionize` but do not tell it to generate any docs/redoc routes.
Using the `callback`, we instead generate our own docs/redoc routes with HTTP basic auth.
'''
versions = versionize(
    app=app,
    prefix_format='/v{major}',
    callback=callback,
    enable_latest=True
)
