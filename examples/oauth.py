from typing_extensions import Annotated
from fastapi import FastAPI, APIRouter, Depends
from fastapi_versionizer import Versionizer
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
from fastapi.security import OAuth2


oauth2_scheme = OAuth2(
    flows=OAuthFlows(
        implicit=OAuthFlowImplicit(
            authorizationUrl='https://login.something.com/authorize',
        )
    ),
    auto_error=True
)

app = FastAPI(
    redoc_url=None,
    swagger_ui_init_oauth={
        'clientId': 'my-client-id',
        'scopes': 'required_scopes',
    }
)


router = APIRouter(prefix='/test')


@router.get('')
def get_test(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


app.include_router(router)

versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    sort_routes=True
).versionize()
