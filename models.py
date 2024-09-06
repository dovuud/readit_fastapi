from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Many-to-Many relationship uchun yordamchi jadval
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), unique=True, index=True)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), unique=True, index=True)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), unique=True, index=True)
    image = Column(String, nullable=True)
    profession = Column(String(212), nullable=True)
    description = Column(Text, nullable=True)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(212), index=True)
    image = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    author_id = Column(Integer, ForeignKey("authors.id"))

    category = relationship("Category", backref="posts")
    author = relationship("Author", backref="posts")
    tags = relationship("Tag", secondary=post_tags, backref="posts")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    name = Column(String(212))
    email = Column(String(212))
    website = Column(String(212), nullable=True)
    message = Column(Text, nullable=True)
    image = Column(String, nullable=True)

    post = relationship("Post", backref="comments")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(212), nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String(212), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(212), nullable=False)
    phone = Column(String(212), nullable=False)
    email = Column(String, nullable=False)
    website = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())