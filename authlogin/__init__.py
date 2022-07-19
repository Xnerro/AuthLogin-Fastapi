__version__ = "0.1.0"
# import all and this run if use poetry
# if not use poetry change some package for run the import
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlogin.src.__init__ import *
from authlogin.src.routes.users import route
from authlogin.src.handle.users import HandUser
import uvicorn

app = FastAPI(title="AuthLogin")

# make static file for css, js or image
app.mount("/static", StaticFiles(directory="authlogin/static"), name="static")

# add session middleware for access session storage
app.add_middleware(SessionMiddleware, secret_key="sdfknsdifugsjdf")

# add directori for templates
pubilc = Jinja2Templates(directory="authlogin/public")

# add all route
app.include_router(route)

# if table not exist it will created
Base.metadata.create_all(engine)
