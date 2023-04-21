import datetime
from typing import Any, Tuple
from fastapi import FastAPI
from fastapi_versionizer.versionizer import api_version, versionize

app = FastAPI(
    title='My Versioned API',
    description='Look, I can version my APIs!'
)


@api_version('2023-1-1')
@app.get('/jan')
async def jan() -> Any:
    return 'jan'


@api_version('2023-2-1')
@app.get('/feb')
async def feb() -> Any:
    return 'feb'


@api_version('2023-10-1')
@app.get('/oct')
async def oct() -> Any:
    return 'oct'


def version_sort_key(version: Tuple[Any, Any]) -> datetime.date:
    major, _ = version
    year, month, day = map(int, major.split('-'))
    return datetime.date(year=year, month=month, day=day)


'''
- This will create the following endpoints:
    - /openapi.json
    - /versions

    - /2023-1-1/docs
    - /2023-1-1/openapi.json
    - /2023-1-1/jan
    
    - /2023-2-1/docs
    - /2023-2-1/openapi.json
    - /2023-2-1/jan
    - /2023-2-1/feb
    
    - /2023-10-1/docs
    - /2023-10-1/openapi.json
    - /2023-10-1/jan
    - /2023-10-1/feb
    - /2023-10-1/oct
'''
versions = versionize(
    app=app,
    prefix_format='/{major}',
    version_format='{major}',
    docs_url='/docs',
    default_version=('2023-1-1', 0),
    version_sort_key=version_sort_key
)
