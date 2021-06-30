from typing import Optional
from MySQLdb.connections import Connection
from app.adapters.repositories.family_repository import FamilyRepository
from app.entities.family import Family


class FindLoginUserUseCase:
    def __init__(self, conn: Connection):
        self.family_repository = FamilyRepository(conn)

    def exec(self, twitter_user_id: int, screen_name: str) -> Optional[Family]:
        twitter_id = "@{}".format(screen_name)

        family = self.family_repository.find_by_twitter_id_and_twitter_user_id(twitter_id, twitter_user_id)
        if family is not None:
            return family

        family = self.family_repository.find_by_twitter_id(twitter_id)
        if family is None or (family.twitter_user_id is not None and family.twitter_user_id != twitter_user_id):
            return None

        self.family_repository.update_twitter_user_id_by_id(twitter_user_id, screen_name)
        return family
