from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
import schemas

# Ma'lumotlar bazasini yaratish
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Category CRUD
@app.get("/categories/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Tag CRUD
@app.get("/tags/", response_model=List[schemas.Tag])
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    return tags

@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

# Author CRUD
@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(
        name=author.name,
        image=author.image,
        profession=author.profession,
        description=author.description,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

# Post CRUD
@app.get("/posts/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(
        title=post.title,
        image=post.image,
        body=post.body,
        category_id=post.category_id,
        author_id=post.author_id,
    )
    db_post.tags = db.query(models.Tag).filter(models.Tag.id.in_(post.tag_ids)).all()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Comment CRUD
@app.get("/comments/", response_model=List[schemas.Comment])
def get_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    return comments

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = models.Comment(
        name=comment.name,
        email=comment.email,
        website=comment.website,
        message=comment.message,
        post_id=comment.post_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Contact CRUD
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        message=contact.message,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts_get/", response_model=List[schemas.Contact])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    print(contacts)
    return contacts

# ContactInfo CRUD
@app.get("/contact_info/", response_model=List[schemas.ContactInfo])
def get_contact_info(db: Session = Depends(get_db)):
    contact_info = db.query(models.ContactInfo).order_by(models.ContactInfo.id.desc()).limit(1).all()
    return contact_info

@app.post("/contact_info_create/", response_model=schemas.ContactInfo)
async def create_contact_info(contact_info: schemas.ContactInfoCreate, db: Session = Depends(get_db)):
    db_contact_info = models.ContactInfo(**contact_info.dict())
    db.add(db_contact_info)
    db.commit()
    db.refresh(db_contact_info)
    return db_contact_info