from fastapi import APIRouter, Depends, HTTPException, Request, responses, status
from fastapi.responses import HTMLResponse, JSONResponse
from authlogin.src.handle.users import HandUser
from ..__init__ import AuthJWT, get_db, Session, dumps
from bcrypt import checkpw
from authlogin.src.schemas.users import UserBase
from jwt.exceptions import DecodeError

# make new route for main route in different file
route = APIRouter(prefix="/users", tags=["users"], responses={404: {"msg": "Not Found"}})

# post route for login
# if want to test in swagger delete Depens in UserBase schemas
@route.post("/login", response_class=HTMLResponse)
async def login(
    req: Request,
    user: UserBase = Depends(UserBase.login),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    user_ = HandUser.by_username(db, user.username)
    if user_:
        # checked hashed pw from db and input
        checked = checkpw(user.password.encode(), user_.password.encode())
        if checked:
            # create access jwt token
            access = Authorize.create_access_token(subject=user_.username)
            # make session for access token
            req.session["token"] = access
            # redirect to home if user in database
            return responses.RedirectResponse("../home", status_code=status.HTTP_302_FOUND)
        else:
            raise HTTPException(401, "Password tidak sesuai")
    else:
        raise HTTPException(401, "Username tidak ditemkan")


# post route for register
# if want to test in swagger delete Depens in UserBase schemas
@route.post("/register", response_class=HTMLResponse)
async def register_post(user: UserBase = Depends(UserBase.register), db: Session = Depends(get_db)):
    await HandUser.create_user(db, user)
    return responses.RedirectResponse("../", status_code=status.HTTP_302_FOUND)


@route.get("/logout")
async def logout(req: Request, auth: AuthJWT = Depends()):
    try:
        auth.jwt_required(req.session.get("token"))
        req.session.clear()
        return responses.RedirectResponse("../")
    except DecodeError:
        return JSONResponse({"msg": "not authenticated"}, status_code=401)
