import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from pydantic import BaseModel


class Token(BaseModel):
    username: str = ""
    expire: int = (datetime.now() + timedelta(days=364)).timestamp() # type: ignore

    @staticmethod
    def verify_jwt(jwt_str: str) -> bool:
        try:
            jwt.decode(jwt_str, os.environ.get("AuthKey", ""), verify=True, algorithms=['HS256'])
        except Exception:
            return False

        return True

    @classmethod
    def from_jwt(cls, jwt_str: str) -> Optional['Token']:
        if not jwt_str:
            return None

        try:
            claims = jwt.decode(jwt_str, os.environ.get("AuthKey", ""), algorithms=['HS256'])
        except Exception:
            return None
        return cls(**claims.items()) # type: ignore

    def to_jwt(self):
        claims = {}
        for k, v in self.__dict__.items():
            if v is not None:
                claims[k] = v

        return jwt.encode(claims, os.environ.get("AuthKey", ""), algorithm='HS256')
