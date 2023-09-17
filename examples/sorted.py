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


@app.post('/xxx_do_something', tags=['Something'], response_model=TestModel)
async def do_something(test: TestModel) -> Any:
    return test


@app.post('/bbb_do_something_else', tags=['Something Else'])
async def do_something_else() -> Any:
    return {'message': 'something else'}


@api_version(2)
@app.post('/xxx_do_something', tags=['Something'])
async def do_something_v2() -> Any:
    return {'message': 'something'}


@api_version(2)
@app.post('/aaa_do_something_new', tags=['Something New'])
async def do_something_new() -> Any:
    return {'message': 'something new'}


@api_version(2, 1)
@app.post('/aaa_do_something_new', tags=['Something New'])
async def do_something_newer() -> Any:
    return {'message': 'something newer'}


'''
- Notes:
    - "/v1.0/docs" and "/v2.0/docs" pages are generated, because `docs_url` is given
    - "/versions" is automatically generated

- We test and seek the following endpoints:
    - /v1.0/xxx_do_something
    - /v1.0/bbb_do_something_else
    - /v2.0/xxx_do_something
    - /v2.0/bbb_do_something_else
    - /v2.0/aaa_do_something_new
    - /v2.1/aaa_do_something_new
'''
versions = versionize(
    app=app,
    prefix_format='/v{major}.{minor}',
    docs_url='/docs',
    enable_latest=True,
    latest_prefix='/latest',
    sorted_routes=True
)
