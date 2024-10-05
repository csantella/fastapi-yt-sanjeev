from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=text('now()'))
    owner_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=text('now()'))