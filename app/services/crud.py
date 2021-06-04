from sqlalchemy.orm import Session

from app import models, schemas


def create_post(db: Session, user_id: int, title: str, body: str, url: str):
    db_post = models.Post(title=title, body=body, owner_id=user_id, url=url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()


def post_list(db: Session):
    return db.query(models.Post).all()


def create_comment(db: Session, post_id: int, comment: schemas.CommentBase):
    db_comment = models.Comment(post_id=post_id, **comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
