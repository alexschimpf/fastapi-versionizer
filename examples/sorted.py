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


@api_version(3, 0)
@app.get('/test-route/bbb', tags=['Version 3.0 test route'])
async def test_route_get_01() -> Any:
    return {'message': 'testing natural sort, this should appear below /test-route and below /test-route/aaa'}


@api_version(3, 0)
@app.get('/test-route/aaa', tags=['Version 3.0 test route'])
async def test_route_get_02() -> Any:
    return {'message': 'testing natural sort, this should appear below /test-route'}


@api_version(3, 0)
@app.get('/test-route', tags=['Version 3.0 test route'])
async def test_route_get_03() -> Any:
    return {'message': 'hello world'}


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
    - /v3.0/test-route
    - /v3.0/test-route/aaa
    - /v3.0/test-route/bbb
'''
versions = versionize(
    app=app,
    prefix_format='/v{major}.{minor}',
    docs_url='/docs',
    enable_latest=True,
    latest_prefix='/latest',
    sorted_routes=True
)
