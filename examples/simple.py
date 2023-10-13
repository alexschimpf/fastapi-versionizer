# mypy: disable-error-code="no-any-return"
# flake8: noqa: A003

from typing import List, Any, Dict
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


class Item(BaseModel):
    id: int
    name: str


class ItemV2(BaseModel):
    id: int
    name: str
    cost: int


class DB:
    def __init__(self) -> None:
        self.users: Dict[int, Any] = {}
        self.items: Dict[int, Any] = {}


db = DB()
app = FastAPI(
    title='test',
    docs_url='/swagger',
    openapi_url='/api_schema.json',
    redoc_url=None,
    description='Simple example of FastAPI Versionizer.',
    terms_of_service='https://github.com/alexschimpf/fastapi-versionizer'
)
users_router = APIRouter(
    prefix='/users',
    tags=['Users']
)
items_router = APIRouter(
    prefix='/items',
    tags=['Items']
)


@app.get('/status', tags=['Status'])
def get_status() -> str:
    return 'Ok'


@api_version(1)
@users_router.get('', deprecated=True)
def get_users() -> List[User]:
    return list(db.users.values())


@api_version(1)
@users_router.post('', deprecated=True)
def create_user(user: User) -> User:
    db.users[user.id] = user
    return user


@api_version(1)
@users_router.get('/{user_id}', deprecated=True)
def get_user(user_id: int) -> User:
    return db.users[user_id]


@api_version(2)
@users_router.get('')
def get_users_v2() -> List[UserV2]:
    return list(user for user in db.users.values() if isinstance(user, UserV2))


@api_version(2)
@users_router.post('')
def create_user_v2(user: UserV2) -> UserV2:
    db.users[user.id] = user
    return user


@api_version(2)
@users_router.get('/{user_id}')
def get_user_v2(user_id: int) -> UserV2:
    return db.users[user_id]


@api_version(1)
@items_router.get('', deprecated=True)
def get_items() -> List[Item]:
    return list(db.items.values())


@api_version(1)
@items_router.post('', deprecated=True)
def create_item(item: Item) -> Item:
    db.items[item.id] = item
    return item


@api_version(1, remove_in_major=2)
@items_router.get('/{item_id}', deprecated=True)
def get_item(item_id: int) -> Item:
    return db.items[item_id]


@api_version(2)
@items_router.get('')
def get_items_v2() -> List[ItemV2]:
    return list(item for item in db.items.values() if isinstance(item, ItemV2))


@api_version(2)
@items_router.post('')
def create_item_v2(item: ItemV2) -> ItemV2:
    db.items[item.id] = item
    return item


app.include_router(users_router)
app.include_router(items_router)

app, versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    include_versions_route=True,
    sort_routes=True
).versionize()
