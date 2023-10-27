# mypy: disable-error-code="no-any-return"
# flake8: noqa: A003

from fastapi import FastAPI, APIRouter, WebSocket

from fastapi_versionizer.versionizer import Versionizer, api_version


app = FastAPI(
    title='test',
    docs_url='/swagger',
    openapi_url='/api_schema.json',
    redoc_url=None,
    description='Websocket example of FastAPI Versionizer.',
    terms_of_service='https://github.com/alexschimpf/fastapi-versionizer'
)
chat_router = APIRouter(
    prefix='/chatterbox',
    tags=['Chatting']
)


@api_version(1)
@chat_router.get('', deprecated=True)
def get_explaination() -> str:
    return 'v1'


@api_version(2)
@chat_router.get('')
def get_explaination_v2() -> str:
    return 'v2'

@api_version(1)
@chat_router.websocket('')
async def chatterbox(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        await websocket.send_text(msg)

@api_version(2)
@chat_router.websocket('')
async def chatterbox_v2(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        await websocket.send_text("pong" if msg == "ping" else f"Your message: {msg}")

app.include_router(chat_router)

versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    include_versions_route=True,
    sort_routes=True
).versionize()
