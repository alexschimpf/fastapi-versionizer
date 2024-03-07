from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_versionizer import Versionizer

app = FastAPI()

# This will not work!
app.mount('/examples-not-working', StaticFiles(directory='examples'), name='examples')

versions = Versionizer(
    app=app,
).versionize()

# Only static file mounts added *after* instantiating Versionizer will work
app.mount('/examples', StaticFiles(directory='examples'), name='examples')
