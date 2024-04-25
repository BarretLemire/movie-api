import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from schemas import (
    Movie,
    CreateMovieRequest,
    CreateMovieResponse,
    UpdateMovieRequest,
    UpdateMovieResponse,
    DeleteMovieResponse,
)


movies: list[Movie] = [
    Movie(movie_id=uuid.uuid4(), name="Spider-Man", year=2002),
    Movie(movie_id=uuid.uuid4(), name="Thor: Ragnarok", year=2017),
    Movie(movie_id=uuid.uuid4(), name="Iron Man", year=2008),
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies")
async def get_movies() -> list[Movie]:
    return movies

@app.post("/movies")
async def create_movie(new_movie: CreateMovieRequest) -> CreateMovieResponse:
    new_movie_id = uuid.uuid4()

    new_movie_obj = Movie(movie_id=new_movie_id, name=new_movie.name, year=new_movie.year)

    movies.append(new_movie_obj)

    response_body = {"id": str(new_movie_id)}
    return JSONResponse(content=response_body)

@app.put("/movies/{movie_id}")
async def update_movie(movie_id: uuid.UUID, updated_movie: UpdateMovieRequest) -> UpdateMovieResponse:
    for movie in movies:
        if movie.movie_id == movie_id:
            movie.name = updated_movie.name
            movie.year = updated_movie.year
            return UpdateMovieResponse(success=True)
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: uuid.UUID) -> DeleteMovieResponse:
    global movies 
    initial_length = len(movies)
    movies = [movie for movie in movies if movie.movie_id != movie_id]
    if len(movies) < initial_length:
        return DeleteMovieResponse(success=True)
    else:
        raise HTTPException(status_code=404, detail="Movie not found")