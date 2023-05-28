from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .views import index
from .apis import heartbeat
# from app.core import auth
# from app.routes import views

app = FastAPI()

# # Set all CORS enabled origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(index.router)
app.include_router(heartbeat.router)