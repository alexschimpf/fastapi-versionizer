from typing import Any
from fastapi import FastAPI, APIRouter
from fastapi_versionizer.versionizer import versioned_api_route, versionize

app = FastAPI(
    title='My Versioned API',
    description='Look, I can version my APIs!'
)
router1 = APIRouter(
    prefix='/hey',
    tags=['Something'],
    route_class=versioned_api_route(major=1, minor=0, major_remove=1, minor_remove=1)
)
router2 = APIRouter(
    prefix='/sup',
    tags=['Something Else'],
    route_class=versioned_api_route(major=1, minor=1)
)


@router1.get('/dude')
def dude() -> Any:
    return 'dude'


@router2.get('/dawg')
def dawg() -> Any:
    return 'dawg'


app.include_router(router1)
app.include_router(router2)

'''
- This will create the following endpoints:
    - /openapi.json
    - /versions

    - /v1_0/docs
    - /v1_0/openapi.json
    - /v1_0/hey/dude
    
    - /v1_1/docs
    - /v1_1/openapi.json
    - /v1_1/sup/dawg
'''
versions = versionize(
    app=app,
    prefix_format='/v{major}_{minor}',
    docs_url='/docs'
)
