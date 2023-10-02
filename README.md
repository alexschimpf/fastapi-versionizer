# FastAPI Versionizer

## Credit
This was inspired by [fastapi_versioning](https://github.com/DeanWay/fastapi-versioning).
This project fixes some of the issues with `fastapi_versioning` and adds some additional features.

## Installation
`pip install fastapi-versionizer`

## Examples
You can find examples in the [examples](/examples) directory.

## Summary
<b>FastAPI Versionizer</b> makes API versioning easy.

Here's an example:

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
    return list(db['users'].values())


@api_version(1)
@users_router.post('', deprecated=True)
def create_user(user: User) -> User:
    db['users'][user.id] = user
    return user


@api_version(2)
@users_router.get('')
def get_users_v2() -> List[UserV2]:
    return list(db['users'].values())


@api_version(2)
@users_router.post('')
def create_user_v2(user: UserV2) -> UserV2:
    db['users'][user.id] = user
    return user


app.include_router(users_router)

app, versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    sort_routes=True
).versionize()
```

This will generate the following endpoints:
- GET /openapi.json
- GET /docs
- GET /v1/openapi.json
- GET /v1/docs
- GET /v1/status
- GET /v1/users
- POST /v1/users
- GET /v2/openapi.json
- GET /v2/docs
- GET /v2/status
- GET /v2/users
- POST /v2/users
- GET /latest/openapi.json
- GET /latest/docs
- GET /latest/status
- GET /latest/users
- POST /latest/users

## Details
<b>FastAPI Versionizer</b> works by creating a new FastAPI app with versioned routes and proper docs pages.
Routes are annotated with version information, using the `@api_version` decorator.
Using this decorator, you can specify the version (major and/or minor) that the route was introduced.
You can also specify the first version when the route should be considered deprecated or even removed.
Each new version will include all routes from previous versions that have not been overridden or marked for removal.
An APIRouter will be created for each version, with the URL prefix defined by the `prefix_format` parameter described below,

## Parameters
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
  - For example, if your latest version is 1, and you have routes: "GET /v1/a" and "POST /v1/b", then "GET /latest/a" and "POST /latest/b" will also be added.
- <b>include_main_docs</b>
  - If True, docs page(s) will be created at the root, with all versioned routes included
- <b>include_main_openapi_route</b>
  - If True, an OpenAPI route will be created at the root, with all versioned routes included
- <b>include_version_docs</b>
  - If True, docs page(s) will be created for each version
- <b>include_version_openapi_route</b>
  - If True, an OpenAPI route will be created for each version
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
- See the [Docs Customization](/examples/docs_customization.py) example for more details
