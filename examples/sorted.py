from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_versionizer.versionizer import api_version, versionize


app = FastAPI(
    title='My Versioned API (route-path sorted)',
    description='Look, I can version my APIs and sort the route-paths!',
)


class TestModel(BaseModel):
    something: str


@app.post('/1', tags=['Something'], response_model=TestModel)
async def do_something(test: TestModel) -> Any:
    return test


@app.post('/2', tags=['Something Else'])
async def do_something_else() -> Any:
    return {'message': 'something else'}


@api_version(2)
@app.post('/1', tags=['Something'])
async def do_something_v2() -> Any:
    return {'message': 'something'}


@api_version(10)
@app.post('/10', tags=['Something New'])
async def do_something_new() -> Any:
    return {'message': 'something new'}


@api_version(10, 1)
@app.post('/10', tags=['Something New'])
async def do_something_newer() -> Any:
    return {'message': 'something newer'}


@api_version(10, 1)
@app.post('/10/0', tags=['Something Newe'])
async def do_something_newest() -> Any:
    return {'message': 'something newest'}


'''
- Notes:
    - "/v1.0/docs", "/v2.0/docs", "/v10.0/docs", and "/v10.1/docs" pages are generated, because `docs_url` is given
    - "/versions" is automatically generated

- We test and seek the following endpoints:
    - /v1.0/1
    - /v1.0/2
    - /v2.0/1
    - /v2.0/2
    - /v10.0/1
    - /v10.0/2
    - /v10.0/10
    - /v10.1/1
    - /v10.1/2
    - /v10.1/10
    - /v10.1/10/0
'''
versions = versionize(
    app=app,
    prefix_format='/v{major}.{minor}',
    docs_url='/docs',
    enable_latest=True,
    latest_prefix='/latest',
    sorted_routes=True
)
