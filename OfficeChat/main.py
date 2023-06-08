from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from OfficeChat.views import index
from OfficeChat.core import Auth2,config


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
app.include_router(config.router)
