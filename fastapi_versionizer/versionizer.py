from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple, TypeVar, cast, Union, Type
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute, Mount
from starlette.routing import BaseRoute, Route, WebSocketRoute
from pydantic import BaseModel
from natsort import natsorted

CallableT = TypeVar('CallableT', bound=Callable[..., Any])
FastAPIT = TypeVar('FastAPIT', bound=FastAPI)


class VersionModel(BaseModel):
    version: str


class VersionsModel(BaseModel):
    versions: List[VersionModel]


def api_version(
    major: int,
    minor: int = 0
) -> Callable[[CallableT], CallableT]:
    """
    Annotates a route as being available from the given version onward (until a
    new version of the route is assigned)
    """

    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor)  # type: ignore
        return func

    return decorator


def api_version_remove(
    major: int,
    minor: int = 0
) -> Callable[[CallableT], CallableT]:
    """
    Annotates a route as being removed from the given version onward (until a
    new version of the route is assigned again)
    """

    def decorator(func: CallableT) -> CallableT:
        func._api_version_remove = (major, minor)  # type: ignore
        return func

    return decorator


def versioned_api_route(
    major: Union[int, None] = None,
    minor: int = 0,
    major_remove: Union[int, None] = None,
    minor_remove: int = 0,
    route_class: Type[APIRoute] = APIRoute
) -> Type[APIRoute]:
    """
    The result of this can be used as the `route_class` for an APIRouter object
    Example:
        APIRouter(
            prefix="/something",
            tags=["Something"],
            route_class=versioned_api_route(major=1, minor=1)
        )
    """

    class VersionedAPIRoute(route_class):  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            try:
                if major is not None:
                    self.endpoint._api_version = (major, minor)
                if major_remove is not None:
                    self.endpoint._api_version_remove = (major_remove, minor_remove)
            except AttributeError:
                # Support bound methods
                if major is not None:
                    self.endpoint.__func__._api_version = (major, minor)
                if major_remove is not None:
                    self.endpoint.__func__._api_version_remove = (major_remove, minor_remove)

    return VersionedAPIRoute


def versionize(
    app: FastAPI,
    version_format: str = '{major}.{minor}',
    prefix_format: str = '/v{major}_{minor}',
    default_version: Tuple[int, int] = (1, 0),
    enable_latest: bool = False,
    latest_prefix: str = '/latest',
    sorted_routes: bool = False,
    get_openapi: Union[Callable[[FastAPI, Tuple[int, int]], Dict[str, Any]], None] = None,
    get_docs: Union[Callable[[Tuple[int, int]], HTMLResponse], None] = None,
    get_redoc: Union[Callable[[Tuple[int, int]], HTMLResponse], None] = None,
    callback: Union[Callable[[FastAPI, Tuple[int, int], str], None], None] = None,
    **kwargs: Any
) -> List[Tuple[int, int]]:
    """
    Mounts a sub-application to the given FastAPI app for each API version.
    The API versions are defined by your use of the @api_version decorator.

    :param app:
    :param version_format:
        - Defines the format for your API versions
        - This is used to display the version in your docs pages
    :param prefix_format:
        - Defines the format used to prefix your versioned route paths
    :param default_version:
        - This will be applied to all routes without the @api_version decorator
    :param enable_latest:
        - Adds "/latest" endpoints, which is an alias for the latest version endpoints
    :param latest_prefix:
        - Defines the prefix use for the "latest" endpoints (if `enabled_latest` is True)
        - This cannot be "/"
    :param sorted_routes:
        - Sort the routes within a version to occur by route-path-name
    :param get_openapi:
        - A function that takes in a versioned FastAPI sub-application and a version (in tuple forms)
        - and returns an OpenAPI schema dict.
        - This will be used to override the `openapi` function of each versioned FastAPI sub-application.
        - This is useful if you want to customize your OpenAPI schemas at runtime
    :param get_docs:
        - A function that takes in a version (in tuple form) and returns an HTML response
        - This is used to generate the Swagger docs for each version
        - You will likely want to use `fastapi.openapi.docs.get_swagger_ui_html` for this
        - This page's URL path will be derived from kwargs['docs_url']
    :param get_redoc:
        - A function that takes in a version (in tuple form) and returns an HTML response
        - This is used to generate the Redoc docs for each version
        - You will likely want to use `fastapi.openapi.docs.get_redoc_html` for this
        - This page's URL path will be derived from kwargs['redoc_url']
    :param callback:
        - A function that takes in 3 arguments: a FastAPI app, its version, and the version path prefix
        - This function should return nothing
        - This is called each time a FastAPI versioned app is created but before being mounted
        - This includes when the "latest" app is created (when enable_latest=True)
    :param kwargs:
        - These are additional arguments that will be applied to each mounted, versioned app
        - For example, if you want to use `swagger_ui_parameters` for all version docs pages, you would
        - set this in kwargs.
    :return list of versions (in tuple form)
    """

    if latest_prefix == '/':
        raise ValueError('latest_prefix cannot be "/"')

    version_route_mapping = _get_version_route_mapping(app=app, default_version=default_version)
    version_remove_route_mapping = _get_version_remove_route_mapping(app=app)

    unique_routes: Dict[Tuple[str, str], BaseRoute] = {}
    versions = sorted(set(version_route_mapping.keys()) | set(version_remove_route_mapping.keys()))
    for version in versions:
        major, minor = version
        prefix = prefix_format.format(major=major, minor=minor)
        semver = version_format.format(major=major, minor=minor)

        for route in version_route_mapping[version]:
            for unique_key in _get_unique_route_keys(route):
                unique_routes[unique_key] = route

        for route in version_remove_route_mapping[version]:
            for unique_key in _get_unique_route_keys(route):
                if unique_key in unique_routes:
                    del unique_routes[unique_key]
                else:
                    raise ValueError(f"Route {unique_key!r} can't be removed in version {version}")

        versioned_app = _build_versioned_app(
            app=app,
            version=version,
            semver=semver,
            unique_routes=dict(natsorted(unique_routes.items())) if sorted_routes else unique_routes,
            prefix=prefix,
            get_openapi=get_openapi,
            get_docs=get_docs,
            get_redoc=get_redoc,
            callback=callback,
            **kwargs
        )
        app.mount(path=prefix, app=versioned_app, name=prefix[1:])

    if enable_latest:
        version = versions[-1]
        major, minor = version
        semver = version_format.format(major=major, minor=minor)
        versioned_app = _build_versioned_app(
            app=app,
            version=version,
            semver=semver,
            unique_routes=dict(natsorted(unique_routes.items())) if sorted_routes else unique_routes,
            prefix=latest_prefix,
            get_openapi=get_openapi,
            get_docs=get_docs,
            get_redoc=get_redoc,
            callback=callback,
            **kwargs
        )
        app.mount(path=latest_prefix, app=versioned_app, name=latest_prefix[1:])

    app.router.routes = [
        route for route in app.routes
        if isinstance(route, Mount) or (isinstance(route, Route) and route.path == app.openapi_url)
    ]

    @app.get('/versions', response_model=VersionsModel, tags=['Versions'])
    async def get_versions_() -> VersionsModel:
        return VersionsModel(versions=[
            VersionModel(
                version=version_format.format(major=major, minor=minor)
            ) for (major, minor) in versions
        ])

    return versions


def _get_unique_route_keys(route: BaseRoute) -> List[Tuple[str, str]]:
    result = []
    if isinstance(route, APIRoute):
        for method in route.methods:
            result.append((route.path, method))
    elif isinstance(route, WebSocketRoute):
        result.append((route.path, ''))
    return result


def _get_version_route_mapping(
    app: FastAPI,
    default_version: Tuple[int, int]
) -> Dict[Tuple[int, int], List[BaseRoute]]:
    version_route_mapping: Dict[Tuple[int, int], List[BaseRoute]] = defaultdict(list)
    version_routes = [
        _version_to_route(route=route, default_version=default_version) for route in app.routes
    ]

    for version, route in version_routes:
        version_route_mapping[version].append(route)

    return version_route_mapping


def _version_to_route(
    route: BaseRoute,
    default_version: Tuple[int, int],
) -> Tuple[Tuple[int, int], BaseRoute]:
    api_route = cast(Route, route)
    version = getattr(api_route.endpoint, '_api_version', default_version)
    return version, api_route


def _get_version_remove_route_mapping(
    app: FastAPI,
) -> Dict[Tuple[int, int], List[BaseRoute]]:
    version_remove_route_mapping: Dict[Tuple[int, int], List[BaseRoute]] = defaultdict(list)
    version_remove_routes = [_version_remove_to_route(route=route) for route in app.routes]

    for version, route in version_remove_routes:
        if version is not None:
            version_remove_route_mapping[version].append(route)

    return version_remove_route_mapping


def _version_remove_to_route(
    route: BaseRoute,
) -> Tuple[Union[Tuple[int, int], None], BaseRoute]:
    api_route = cast(Route, route)
    version = getattr(api_route.endpoint, '_api_version_remove', None)
    return version, api_route


def _build_versioned_app(
    app: FastAPIT,
    version: Tuple[int, int],
    semver: str,
    unique_routes: Dict[Tuple[str, str], BaseRoute],
    prefix: str,
    get_openapi: Union[Callable[[FastAPI, Tuple[int, int]], Dict[str, Any]], None] = None,
    get_docs: Union[Callable[[Tuple[int, int]], HTMLResponse], None] = None,
    get_redoc: Union[Callable[[Tuple[int, int]], HTMLResponse], None] = None,
    callback: Union[Callable[[FastAPI, Tuple[int, int], str], None], None] = None,
    **kwargs: Any
) -> FastAPIT:
    docs_url = kwargs.pop('docs_url', None)
    redoc_url = kwargs.pop('redoc_url', None)
    versioned_app = app.__class__(
        title=app.title,
        description=app.description,
        version=semver,
        docs_url=docs_url if not get_docs else None,
        redoc_url=redoc_url if not get_redoc else None,
        **kwargs
    )
    versioned_app.dependency_overrides = app.dependency_overrides
    for route in unique_routes.values():
        if isinstance(route, Route) and \
                ((get_docs and route.path == app.docs_url) or (get_redoc and route.path == app.redoc_url)):
            # Doc pages will be added later
            continue
        versioned_app.router.routes.append(route)

    if get_openapi:
        def openapi() -> Dict[str, Any]:
            return get_openapi(versioned_app, version)
        versioned_app.openapi = openapi  # type: ignore

    if get_docs and docs_url:
        @versioned_app.get(cast(str, docs_url), include_in_schema=False)
        def get_docs_() -> HTMLResponse:
            return get_docs(version)

    if get_redoc and redoc_url:
        @versioned_app.get(cast(str, redoc_url), include_in_schema=False)
        def get_redoc_() -> HTMLResponse:
            return get_redoc(version)

    if callback:
        callback(versioned_app, version, prefix)

    return versioned_app
