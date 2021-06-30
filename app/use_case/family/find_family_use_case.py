from typing import Optional
from MySQLdb.connections import Connection
from app.adapters.repositories.family_repository import FamilyRepository
from app.entities.family import Family


class FindFamilyUseCase:
    def __init__(self, conn: Connection):
        self.family_repository = FamilyRepository(conn)

    def exec(self, twitter_id: str):
        return self.family_repository.find_by_twitter_id(twitter_id)