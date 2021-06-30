import datetime
from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class Family(UserMixin):
    id: str
    twitter_user_id: str
    is_using: bool
    main_id: str
    atcoder_id: str
    rating: int
    is_hidden: bool
    rate_hidden: bool
    comment: str
    birthday: datetime.date

    def get_id(self):
        return self.id
