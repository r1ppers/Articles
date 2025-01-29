import datetime
from pydantic import Field, field_validator
from datetime import date, datetime

class AuthorBase():
    birth_date: date


    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, birth_date: date):
        if birth_date.year >= datetime.now().date().year:
            return 'error'
        return 'birth_date'

AuthorBase.birth_date = datetime.now()
print(AuthorBase.validate_birth_date(AuthorBase.birth_date))