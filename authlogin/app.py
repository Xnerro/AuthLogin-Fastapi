from .__init__ import *
import jwt

# exception for jwt token
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# route login and will render login templates
@app.get("/", response_class=HTMLResponse)
def root(req: Request):
    return pubilc.TemplateResponse("login.html", {"request": req})


# route for home
# protec route  with function jwt_required(), which requires token
# decode token for get the subject
@app.get("/home", response_class=HTMLResponse)
def home(req: Request, auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    auth.jwt_required(req.session.get("token"))
    x = jwt.decode(req.session.get("token"), options={"verify_signature": False})
    user = HandUser.by_username(db, x["sub"])
    return pubilc.TemplateResponse("home.html", {"request": req, "user": user})


# route Register and will render Register templates
@app.get("/register", response_class=HTMLResponse)
def register(req: Request):
    return pubilc.TemplateResponse("register.html", {"request": req})


# funcion to start fastapi with uvicorn
def start():
    uvicorn.run("authlogin.app:app", reload=True, port=3000)

# run function if not use poetry
# start()
