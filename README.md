# FastAPI Versionizer

## Credit
This was inspired by [fastapi_versioning](https://github.com/DeanWay/fastapi-versioning).
This project addresses issues with `fastapi_versioning` and adds some additional features.

## Installation
`pip install fastapi-versionizer`

## Examples
You can find examples in the [examples](https://github.com/alexschimpf/fastapi-versionizer/tree/main/examples) directory.

## Summary
<b>FastAPI Versionizer</b> makes API versioning easy.

Here is a simple (and rather contrived) example:

```python
from typing import List
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from fastapi_versionizer.versionizer import Versionizer, api_version


class User(BaseModel):
    id: int
    name: str


class UserV2(BaseModel):
    id: int
    name: str
    age: int


db = {
    'users': {}
}
app = FastAPI(
    title='test',
    redoc_url=None
)
users_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@app.get('/status', tags=['Status'])
def get_status() -> str:
    return 'Ok'


@api_version(1)
@users_router.get('', deprecated=True)
def get_users() -> List[User]:
    return list(user for user in db['users'].values() if isinstance(user, User))


@api_version(1)
@users_router.post('', deprecated=True)
def create_user(user: User) -> User:
    db['users'][user.id] = user
    return user


@api_version(2)
@users_router.get('')
def get_users_v2() -> List[UserV2]:
    return list(user for user in db['users'].values() if isinstance(user, UserV2))


@api_version(2)
@users_router.post('')
def create_user_v2(user: UserV2) -> UserV2:
    db['users'][user.id] = user
    return user


app.include_router(users_router)

versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    sort_routes=True
).versionize()
```

This will generate the following endpoints:
- <b>GET /openapi.json</b>
  - OpenAPI schema with endpoints from all versions
- <b>GET /docs</b>
  - Swagger page with endpoints from all versions
- <b>GET /v1/openapi.json</b>
  - OpenAPI schema for v1 endpoints
- <b>GET /v1/docs</b>
  - Swagger page for v1 endpoints
- <b>GET /v1/status</b>
- <b>GET /v1/users</b>
- <b>POST /v1/users</b>
- <b>GET /v2/openapi.json</b>
  - OpenAPI schema for v2 endpoints
- <b>GET /v2/docs</b>
  - Swagger page for v2 endpoints
- <b>GET /v2/status</b>
  - This gets carried on from v1, where it was introduced, but has the same implementation
- <b>GET /v2/users</b>
- <b>POST /v2/users</b>
- <b>GET /latest/openapi.json</b>
  - OpenAPI schema for latest (i.e. v2) endpoints
- <b>GET /latest/docs</b>
  - Swagger page for latest (i.e. v2) endpoints
- <b>GET /latest/status</b>
- <b>GET /latest/users</b>
- <b>POST /latest/users</b>

## Details
<b>FastAPI Versionizer</b> works by modifying a FastAPI app in place, adding versioned routes and proper docs pages.
Routes are annotated with version information, using the `@api_version` decorator.
Using this decorator, you can specify the version (major and/or minor) that the route was introduced.
You can also specify the first version when the route should be considered deprecated or even removed.
Each new version will include all routes from previous versions that have not been overridden or marked for removal.
An APIRouter will be created for each version, with the URL prefix defined by the `prefix_format` parameter described below,

## Versionizer Parameters
- <b>app</b>
  - The FastAPI you want to version
- <b>prefix_format</b>
  - Used to build the version path prefix for routes.
  - It should contain either "{major}" or "{minor}" or both.
  - Examples: "/v{major}", "/v{major}_{minor}"
- <b>semantic_version_format</b>
  - Used to build the semantic version, which is shown in docs.
  - Examples: "{major}", "{major}.{minor}"
- <b>default_version</b>
  - Default version used if a route is not annotated with @api_version.
- <b>latest_prefix</b>
  - If this is given, the routes in your latest version will be a given a separate prefix alias.
  - For example, if latest_prefix='latest', latest version is 1, and you have routes: "GET /v1/a" and "POST /v1/b", then "GET /latest/a" and "POST /latest/b" will also be added.
- <b>include_main_docs</b>
  - If True, docs page(s) will be created at the root, with all versioned routes included
- <b>include_main_openapi_route</b>
  - If True, an OpenAPI route will be created at the root, with all versioned routes included
- <b>include_version_docs</b>
  - If True, docs page(s) will be created for each version
- <b>include_version_openapi_route</b>
  - If True, an OpenAPI route will be created for each version
- <b>include_versions_route</b>
  - If True, a "GET /versions" route will be added, which includes information about all API versions
- <b>sort_routes</b>
  - If True, all routes will be naturally sorted by path within each version.
  - If you have included the main docs page, the routes are sorted within each version, and versions are sorted from earliest to latest. If you have added a "latest" alias, its routes will be listed last.
- <b>callback</b>
  - A function that is called each time a version router is created and all its routes have been added.
  - It is called before the router has been added to the root FastAPI app.
  - This function should not return anything and has the following parameters:
    - Version router
    - Version (in tuple form)
    - Version path prefix

## Docs Customization
- There are various parameters mentioned above for controlling which docs page are generated.
- The swagger and redoc URL paths can be controlled by setting your FastAPI app's `docs_url` and `redoc_url`.
  - If these are set to None, docs pages will not be generated.
- Swagger UI parameters can be controlled by setting your FastAPI app's `swagger_ui_parameters`
- If you want to customize your docs beyond what <b>FastAPI Versionizer</b> can handle, you can do the following:
  - Set `include_main_docs` and `include_version_docs` to False
  - Set `include_main_openapi_route` and `include_version_openapi_route` to False if you need to customize the OpenAPI schema.
  - Pass a `callback` param to `Versionizer` and add your own docs/OpenAPI routes manually for each version
  - If you want a "main" docs page, with all versioned routes included, you can manually add a docs/OpenAPI route to the versioned FastAPI app returned by `Versionizer.versionize()`.
- See the [Docs Customization](https://github.com/alexschimpf/fastapi-versionizer/tree/main/examples/docs_customization.py) example for more details

## Gotchas

### Static file mounts

If you need to [mount static files](https://fastapi.tiangolo.com/tutorial/static-files/), you'll have to add those to
your FastAPI app **after** instantiating Versionizer. See the [Static file mount](https://github.com/alexschimpf/fastapi-versionizer/tree/main/examples/with_static_file_mount.py)
example for more details.
