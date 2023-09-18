from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime

from app.services.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    personal_code = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, personal_code={self.personal_code})>"
