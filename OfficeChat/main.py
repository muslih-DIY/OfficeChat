from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from FastApiTemplate.views import index
from FastApiTemplate.apis import heartbeat
from FastApiTemplate.core import Auth2,config
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
app.include_router(config.router)
# app.include_router(Auth2.app)