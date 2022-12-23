from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_versionizer.versionizer import api_version, versionize


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


@api_version(2)
@app.post('/do_something_new', tags=['Something New'])
async def do_something_new() -> Any:
    return {'message': 'something new'}


'''
- Notes:
    - "/v1/docs" and "/v2/docs" pages are generated, because `docs_url` is given
    - "/v1/redoc" and "/v2/redoc" pages are generated because `redoc_url` is given
    - "/versions" is automatically generated

- This will create the following endpoints:
    - /openapi.json
    - /versions
    - /v1/docs
    - /v1/redoc
    - /v1/openapi.json
    - /v1/do_something
    - /v1/do_something_else
    - /v2/docs
    - /v2/redoc
    - /v2/openapi.json    
    - /v2/do_something
    - /v2/do_something_else
    - /v2/do_something_new
'''
versions = versionize(
    app=app,
    prefix_format='/v{major}',
    docs_url='/docs',
    redoc_url='/redoc'
)
