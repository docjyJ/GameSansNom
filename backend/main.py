from typing import Self
from uuid import uuid4, UUID

from cachetools import TTLCache
from fastapi import FastAPI, HTTPException, status


app = FastAPI()


class GameData:
    cache = TTLCache[UUID, Self](maxsize=64, ttl=3600)

    def __init__(self):
        self.token_pink: UUID = uuid4()
        self.token_black: UUID | None = None

    @classmethod
    def new(cls) -> tuple[UUID, Self]:
        game_id = uuid4()
        game_data = cls()
        cls.cache[game_id] = game_data
        return game_id, game_data

    @classmethod
    def get(cls, game_id: UUID) -> Self:
        game_data = cls.cache[game_id]
        if game_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"The game with id '{game_id}' does not exist."
            )
        return game_data

    def join(self) -> UUID:
        if self.token_black is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The game is already joined by a player."
            )
        self.token_black = uuid4()
        return self.token_black

@app.get("/api/v1/games/new", status_code=status.HTTP_201_CREATED)
async def create_game():
    game_id, game_data = GameData.new()
    return {
        "game_id": game_id,
        "token_pink": game_data.token_pink,
    }


@app.get("/api/v1/games/{game_id}/join", status_code=status.HTTP_202_ACCEPTED)
async def join_game(game_id: UUID):
    game_data = GameData.get(game_id)
    black_token = game_data.join()
    return {
        "token_black": black_token
    }


