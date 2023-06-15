from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apis import docs
from views import index
from core import auth
from core import config
from views import socket
from depends.database import create_all_table

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
    auth.router,
    socket.router
)
for route in routes:
    app.include_router(route)


@app.on_event('startup')
async def start():
    create_all_table()