from collections import defaultdict
from enum import Enum
from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
import fastapi.openapi.utils
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRoute, APIWebSocketRoute
from natsort import natsorted
from typing import Any, Callable, Dict, List, Tuple, TypeVar, Union, cast, Set

CallableT = TypeVar('CallableT', bound=Callable[..., Any])


def api_version(
    major: int,
    minor: int = 0,
    deprecate_in_major: Union[int, None] = None,
    deprecate_in_minor: int = 0,
    remove_in_major: Union[int, None] = None,
    remove_in_minor: int = 0
) -> Callable[[CallableT], CallableT]:
    """
    Annotates a route as being available from the given version onward (until a
    new version of the route is assigned)
    """

    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor)  # type: ignore
        if deprecate_in_major is not None:
            func._deprecate_in_version = (deprecate_in_major, deprecate_in_minor)  # type: ignore
        if remove_in_major is not None:
            func._remove_in_version = (remove_in_major, remove_in_minor)  # type: ignore
        return func

    return decorator


class Versionizer:

    def __init__(
        self,
        app: FastAPI,
        prefix_format: str = '/v{major}_{minor}',
        semantic_version_format: str = '{major}.{minor}',
        default_version: Tuple[int, int] = (1, 0),
        latest_prefix: Union[str, None] = None,
        include_main_docs: bool = True,
        include_main_openapi_route: bool = True,
        include_version_docs: bool = True,
        include_version_openapi_route: bool = True,
        include_versions_route: bool = False,
        sort_routes: bool = False,
        callback: Union[Callable[[APIRouter, Tuple[int, int], str], None], None] = None
    ):
        """
        :param app:
        :param prefix_format:
            Used to build the version path prefix for routes.
            It should contain either "{major}" or "{minor}" or both.
        :param semantic_version_format:
            Used to build the semantic version, which is shown in docs.
        :param default_version:
            Default version used if a route is not annotated with @api_version.
        :param latest_prefix:
            If this is given, the routes in your latest version will be a given a separate prefix alias.
            For example, if latest_prefix='latest', latest version is 1, and you have routes:
            "GET /v1/a" and "POST /v1/b", then "GET /latest/a" and "POST /latest/b" will also be added.
        :param include_main_docs:
            If True, docs page(s) will be created at the root, with all versioned routes included
        :param include_main_openapi_route:
            If True, an openapi route will be created at the root, with all versioned routes included
        :param include_version_docs:
            If True, docs page(s) will be created for each version
        :param include_version_openapi_route:
            If True, an openapi route will be created for each version
        :param include_versions_route:
            If True, a "GET /versions" route will be added, which includes information about all API versions
        :param sort_routes:
            If True, all routes will be naturally sorted by path within each version.
            If you have included the main docs page, the routes are sorted within each version, and versions
            are sorted from earliest to latest. If you have added a "latest" alias, its routes will be listed last.
        :param callback:
            A function that is called each time a version router is created and all its routes have been added.
            It is called before the router has been added to the root FastAPI app.
            This function should not return anything and has the following parameters:
                - Version router
                - Version (in tuple form)
                - Version path prefix
        """
        self._app = app
        self._original_app_routes = app.routes
        self._prefix_format = prefix_format
        self._semantic_version_format = semantic_version_format
        self._default_version = default_version
        self._latest_prefix = latest_prefix
        self._include_main_docs = include_main_docs
        self._include_main_openapi_route = include_main_openapi_route
        self._include_version_docs = include_version_docs
        self._include_version_openapi_route = include_version_openapi_route
        self._include_versions_route = include_versions_route
        self._sort_routes = sort_routes
        self._callback = callback

        self._strip_routes()

    def versionize(self) -> List[Tuple[int, int]]:
        """
        Versions your FastAPI application, in place.

        :returns: list of all versions (each in tuple form)
        """

        version, routes_by_key = None, None
        routes_by_version = self._get_routes_by_version()
        versions = list(routes_by_version.keys())
        for version, routes_by_key in routes_by_version.items():
            major, minor = version
            version_prefix = self._prefix_format.format(major=major, minor=minor)
            version_router = self._build_version_router(
                version=version,
                version_prefix=version_prefix,
                routes_by_key=routes_by_key
            )
            if self._callback:
                self._callback(version_router, version, version_prefix)
            self._app.include_router(router=version_router)

        if self._latest_prefix is not None and routes_by_key and version:
            latest_router = self._build_version_router(
                version=version,
                version_prefix=self._latest_prefix,
                routes_by_key=routes_by_key
            )
            if self._callback:
                self._callback(latest_router, version, self._latest_prefix)
            self._app.include_router(router=latest_router)

        if self._include_versions_route:
            self._add_versions_route(versions=versions)

        return versions

    def _build_api_url(self, version_prefix: str, path: str) -> str:
        root_path = (self._app.root_path or '').rstrip('/')
        return f'{root_path}{version_prefix}{path}'

    def _build_version_router(
        self,
        version: Tuple[int, int],
        version_prefix: str,
        routes_by_key: Dict[Tuple[str, str], Union[APIRoute, APIWebSocketRoute]]
    ) -> APIRouter:
        router = APIRouter(
            prefix=version_prefix
        )
        routes_by_key = dict(natsorted(routes_by_key.items())) if self._sort_routes else routes_by_key
        for route in routes_by_key.values():
            self._add_route_to_router(route=route, router=router, version=version)

        self._add_version_docs(
            router=router,
            version=version,
            version_prefix=version_prefix
        )

        return router

    def _get_routes_by_version(
        self
    ) -> Dict[Tuple[int, int], Dict[Tuple[str, str], Union[APIRoute, APIWebSocketRoute]]]:
        routes_by_start_version: Dict[Tuple[int, int], List[Union[APIRoute, APIWebSocketRoute]]] = defaultdict(list)
        for route in self._original_app_routes:
            if isinstance(route, (APIRoute, APIWebSocketRoute)):
                version = getattr(route.endpoint, '_api_version', self._default_version)
                routes_by_start_version[version].append(route)

        routes_by_end_version: Dict[Tuple[int, int], List[Union[APIRoute, APIWebSocketRoute]]] = defaultdict(list)
        for route in self._original_app_routes:
            if isinstance(route, (APIRoute, APIWebSocketRoute)):
                version = getattr(route.endpoint, '_remove_in_version', None)
                if version:
                    routes_by_end_version[version].append(route)

        versions = sorted(set(routes_by_start_version.keys()))
        routes_by_version: Dict[Tuple[int, int], Dict[Tuple[str, str], Union[APIRoute, APIWebSocketRoute]]] = {}
        curr_version_routes_by_key: Dict[Tuple[str, str], Union[APIRoute, APIWebSocketRoute]] = {}
        for version in versions:
            for route in routes_by_start_version[version]:
                route_keys = self._get_route_keys(route=route)
                curr_version_routes_by_key.update(route_keys)

            for route in routes_by_end_version[version]:
                route_keys = self._get_route_keys(route=route)
                for route_key, method_route in route_keys.items():
                    del curr_version_routes_by_key[route_key]

            routes_by_version[version] = dict(curr_version_routes_by_key)

        return routes_by_version

    @classmethod
    def _get_route_keys(
        cls,
        route: Union[APIRoute, APIWebSocketRoute]
    ) -> Dict[Tuple[str, str], Union[APIRoute, APIWebSocketRoute]]:
        routes_by_key: Dict[Tuple[str, str], Union[APIRoute, APIWebSocketRoute]] = {}
        if isinstance(route, APIRoute):
            for method in route.methods:
                routes_by_key[(route.path, method)] = route
        elif isinstance(route, APIWebSocketRoute):
            routes_by_key[(route.path, '')] = route

        return routes_by_key

    def _add_version_docs(
        self,
        router: APIRouter,
        version: Tuple[int, int],
        version_prefix: str
    ) -> None:
        version_str = f'v{self._semantic_version_format.format(major=version[0], minor=version[1])}'
        title = f'{self._app.title} - {version_str}'
        tags: Set[Union[str, Enum]] = set()
        versioned_tags: List[Dict[str, Any]] = []

        if self._app.openapi_tags is not None:
            for route in router.routes:
                if isinstance(route, APIRoute):
                    if isinstance(route.tags, list):
                        tags.update(route.tags or ())

            if tags:
                openapi_tags = self._app.openapi_tags or []
                for openapi_tag in openapi_tags:
                    if openapi_tag['name'] in tags:
                        versioned_tags.append(openapi_tag)

        if self._include_version_openapi_route and self._app.openapi_url is not None:
            @router.get(self._app.openapi_url, include_in_schema=False)
            async def get_openapi() -> Any:
                openapi_params: Dict[str, Any] = {
                    'title': title,
                    'version': version_str,
                    'routes': router.routes,
                    'description': self._app.description,
                    'terms_of_service': self._app.terms_of_service,
                    'contact': self._app.contact,
                    'license_info': self._app.license_info,
                    'servers': self._app.servers,
                    'tags': versioned_tags,
                }

                if hasattr(self._app, 'summary'):
                    # Available since OpenAPI 3.1.0, FastAPI 0.99.0
                    openapi_params['summary'] = self._app.summary

                return fastapi.openapi.utils.get_openapi(**openapi_params)

        if self._include_version_docs and self._app.docs_url is not None and self._app.openapi_url is not None:
            openapi_url = self._build_api_url(version_prefix, self._app.openapi_url)
            oauth2_redirect_url = self._build_api_url(
                version_prefix, cast(str, self._app.swagger_ui_oauth2_redirect_url))

            @router.get(self._app.docs_url, include_in_schema=False)
            async def get_docs() -> HTMLResponse:
                return get_swagger_ui_html(
                    openapi_url=openapi_url,
                    title=title,
                    swagger_ui_parameters=self._app.swagger_ui_parameters,
                    init_oauth=self._app.swagger_ui_init_oauth,
                    oauth2_redirect_url=oauth2_redirect_url
                )

            if self._app.swagger_ui_oauth2_redirect_url:
                @router.get(self._app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
                async def get_oauth2_redirect() -> HTMLResponse:
                    return get_swagger_ui_oauth2_redirect_html()

        if self._include_version_docs and self._app.redoc_url is not None and self._app.openapi_url is not None:
            @router.get(self._app.redoc_url, include_in_schema=False)
            async def get_redoc() -> HTMLResponse:
                openapi_url = self._build_api_url(version_prefix, cast(str, self._app.openapi_url))
                return get_redoc_html(
                    openapi_url=openapi_url,
                    title=title
                )

    def _add_versions_route(self, versions: List[Tuple[int, int]]) -> None:
        @self._app.get(
            '/versions',
            tags=['Versions'],
            response_class=JSONResponse
        )
        def get_versions() -> Dict[str, Any]:
            version_models: List[Dict[str, Any]] = []
            for (major, minor) in versions:
                version_prefix = self._prefix_format.format(major=major, minor=minor)
                version_str = self._semantic_version_format.format(major=major, minor=minor)

                version_model = {
                    'version': version_str,
                }

                if self._include_version_openapi_route and self._app.openapi_url is not None:
                    version_model['openapi_url'] = self._build_api_url(version_prefix, self._app.openapi_url)

                if self._include_version_docs and self._app.docs_url is not None:
                    version_model['swagger_url'] = self._build_api_url(version_prefix, self._app.docs_url)

                if self._include_version_docs and self._app.redoc_url is not None:
                    version_model['redoc_url'] = self._build_api_url(version_prefix, self._app.redoc_url)

                version_models.append(version_model)

            return {
                'versions': version_models
            }

    @staticmethod
    def _add_route_to_router(
        route: Union[APIRoute, APIWebSocketRoute],
        router: APIRouter,
        version: Tuple[int, int]
    ) -> None:
        kwargs = dict(route.__dict__)

        deprecated_in_version = getattr(route.endpoint, '_deprecate_in_version', None)
        if deprecated_in_version is not None:
            deprecated_in_major, deprecated_in_minor = deprecated_in_version
            if (
                version[0] >= deprecated_in_major or
                (version[0] == deprecated_in_major and version[1] >= deprecated_in_minor)
            ):
                kwargs['deprecated'] = True

        for _ in range(10000):
            try:
                if isinstance(route, APIRoute):
                    return router.add_api_route(**kwargs)
                elif isinstance(route, APIWebSocketRoute):
                    return router.add_api_websocket_route(**kwargs)
            except TypeError as e:
                e_str = str(e)
                key_start = e_str.index("'") + 1
                key_end = e_str.rindex("'")
                kwargs.pop(e_str[key_start:key_end])

        raise Exception('Failed to add route')

    def _strip_routes(self) -> None:
        paths_to_keep = []
        if self._include_main_docs:
            paths_to_keep.extend([
                self._app.docs_url,
                self._app.redoc_url,
                self._app.swagger_ui_oauth2_redirect_url
            ])
        if self._include_main_openapi_route:
            paths_to_keep.append(self._app.openapi_url)

        self._app.router.routes = [
            route for route in self._app.routes if
            getattr(route, 'path') in paths_to_keep
        ]
