from typing import Optional
from MySQLdb.connections import Connection
from app.entities.family import Family


class FamilyRepository:
    ALL_COLUMNS = "id, twitter_user_id, is_using, main_id, atcoder_id, rating, is_hidden, rate_hidden, " \
                  "comment, birthday"

    def __init__(self, conn: Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def find_by_twitter_id_and_twitter_user_id(self, twitter_id: str, twitter_user_id: int) -> Optional[Family]:
        self.cursor.execute(
            "SELECT {} FROM family WHERE id = %s AND twitter_user_id = %s".format(self.ALL_COLUMNS),
            (twitter_id, twitter_user_id)
        )
        data = self.cursor.fetchone()
        if data is None:
            return None

        return Family(*data)

    def find_by_twitter_id(self, twitter_id: str) -> Optional[Family]:
        self.cursor.execute(
            "SELECT {} FROM family WHERE id = %s".format(self.ALL_COLUMNS),
            (twitter_id,)
        )
        data = self.cursor.fetchone()
        if data is None:
            return None

        return Family(*data)

    def update_twitter_user_id_by_id(self, twitter_user_id: int, twitter_id: str) -> None:
        self.cursor.execute(
            "UPDATE family SET twitter_user_id = %s WHERE id = %s",
            (twitter_user_id, twitter_id)
        )
        self.conn.commit()
