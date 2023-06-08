from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apis import docs
from views import index
from depends import Auths
from core import config

app = FastAPI()

# # Set all CORS enabled origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.mount("/static", StaticFiles(directory=config.ROOT / "static"), name="static")

routes = (
    index.router,
    docs.router,
    Auths.router,
)
for route in routes:
    app.include_router(route)

