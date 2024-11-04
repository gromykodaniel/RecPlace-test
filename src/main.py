from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from src.movies.router import router_movies
from src.user.router import router_auth

app = FastAPI()
app.include_router(router_auth)

app.include_router(router_movies)


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
