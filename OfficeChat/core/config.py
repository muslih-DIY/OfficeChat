
from fastapi.templating import Jinja2Templates
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
import pathlib

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)
ALGORITHM=config('ALGORITHM', cast=str, default="HS256") 
SESSION_EXPIRE_MINUTES=config('SESSION_EXPIRE_MINUTES', cast=int, default=60)  
ACCESS_TOKEN_EXPIRE_MINUTES=config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=10)
  
ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATE = ROOT / "templates"
STATIC = ROOT / "static"
templates = Jinja2Templates(directory=TEMPLATE)
