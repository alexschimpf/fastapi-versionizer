from fastapi import FastAPI

from fastapi_versionizer.versionizer import Versionizer, api_version


app = FastAPI(
    title='test',
    docs_url='/swagger',
    root_path='/api',
    openapi_url='/api_schema.json',
    redoc_url=None,
)


@api_version(1)
@app.get('/status', tags=['Status'])
def get_status_v1() -> str:
    return 'Okv1'


@api_version(2)
@app.get('/status', tags=['Status'])
def get_status_v2() -> str:
    return 'Okv2'


app, versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    include_versions_route=True,
    sort_routes=True
).versionize()
