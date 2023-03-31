from typing import Union, Annotated

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from datetime import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


class User(BaseModel):
    id: int
    name: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/auth/refresh")
def post_refresh_token(Authorize: AuthJWT = Depends()):
    access_token = Authorize.create_access_token(subject=1111)
    refresh_token = Authorize.create_refresh_token(subject=1111)
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "accessTokenExpiresIn": datetime.today().isoformat(),
        "refreshTokenExpiresIn": datetime.today().isoformat(),
    }


@app.post("/auth/access")
def post_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {
        "accessToken": new_access_token,
        "accessTokenExpiresIn": datetime.today().isoformat(),
    }


@app.get("/user")
def get_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return {"id": 1111, "name": "bluejoy"}


@app.get("/ground")
def get_ground(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return {
        "data": [
            {
                "id": 1212312,
                "coordinate": "001234",
                "title": "카톡!",
                "expiresIn": "2023-03-29 17:22:21",
                "maker": {
                    "id": 1111,
                    "name": "dd"
                }
            },
            {
                "id": 1212312,
                "coordinate": "001234",
                "title": "카톡!",
                "expiresIn": "2023-03-29 17:22:21",
                "maker": {
                    "id": 1111,
                    "name": "dd"
                }
            },
            {
                "id": 1212312,
                "coordinate": "001234",
                "title": "카톡!",
                "expiresIn": "2023-03-29 17:22:21",
                "maker": {
                    "id": 1111,
                    "name": "dd"
                }
            }
        ]
    }


class PostGroundDto(BaseModel):
    title: str
    expiresIn: str
    id: int | None = None
    coordinate: str | None = None
    maker: User | None = None


@app.post("/ground")
def get_ground(ground: PostGroundDto, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    ground.maker = User(id=current_user_id, name='bluejoy')
    ground.coordinate = '111000'
    ground.id = 11
    return ground
