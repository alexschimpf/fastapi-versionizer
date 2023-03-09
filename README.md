# FastAPI Versionizer

## Credit
This was inspired by [fastapi_versioning](https://github.com/DeanWay/fastapi-versioning).
This project fixes some of the issues with `fastapi_versioning` and adds some additional features.

## Installation
`pip install fastapi-versionizer`

## Examples
You can find examples in the [examples](https://github.com/alexschimpf/fastapi-versionizer/tree/main/examples) directory.

## Details
- Routes can be annotated using the `@api_version` decorator
  - This essentially says, "This route is available from version (major, minor) onward, until a new version of the route is defined."
- Use the `versionize` function on your FastAPI app to perform the versionizing magic
  - Each version results in a new mounted FastAPI sub-application with a version prefix you define
  - Unlike `fastapi_versioning`, this does not return a new FastAPI app, but applies the versioning directly to the app you provide
  - You can generate a "latest" alias for the latest version using `enable_latest` and `latest_prefix`
  - You can customize your OpenAPI schemas at runtime using `get_openapi`
    - This will be used to override the `openapi` function of all versioned FastAPI sub-applications
  - You can generate each versioned Swagger page using `get_docs` and `docs_url`
    - This is useful if you need to want to customize your Swagger HTML using `fastapi.openapi.docs.get_swagger_ui_html`
    - See the [Advanced Example](https://github.com/alexschimpf/fastapi-versionizer/tree/main/examples/advanced.py) for more details
  - You can generate each versioned Redoc page using `get_redoc` and `redoc_url`
    - This is useful if you need to want to customize your Redoc HTML using `fastapi.openapi.docs.get_redoc_html`
    - The usage of this is very similar to `get_docs`
  - You can sort the routes within a version to occur by route-path-name using `sorted_routes` see 
    the Sorted Example for more details.
  - You can pass additional `kwargs` that will be supplied to each versioned sub-application
    - Note: `app.title` and `app.description` are automatically supplied to each versioned sub-application
    - For all other FastAPI parameters, these must be passed via `kwargs`
    - If you want a custom title and description for each versioned docs page, you can use `get_docs` and/or `get_redoc`
    - Note: If you want docs pages to be generated, you must pass either `docs_url` or `redoc_url` as kwargs
    - Note: If you want to specify custom `responses`, these must be defined on your FastAPI app (not via `kwargs`)
      - See the [Advanced Example](https://github.com/alexschimpf/fastapi-versionizer/tree/main/examples/advanced.py) for more details
