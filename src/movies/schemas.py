from pydantic import BaseModel


class SMovieRequest(BaseModel):
    movie: str


class SMovieRequestDetails(BaseModel):
    movie_id: int
