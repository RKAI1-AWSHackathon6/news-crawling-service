from __future__ import division
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from model.article import Article
from model.newspaper import NewspaperSite
import time
import schemas
import datetime
from pprint import pprint

def create_newspaper_site(db: Session, newspaper_site: schemas.NewspaperSite):
    db_newspaper_site = NewspaperSite(source_url=newspaper_site.source_url, source_rss=newspaper_site.source_rss)
    db.add(db_newspaper_site)
    db.commit()
    db.refresh(db_newspaper_site)
    return db_newspaper_site

def get_newspaper_site(db: Session,limit=10):
    return db.query(NewspaperSite).limit(limit).all()

def get_latest_publish_time(db: Session, source_id):
    return db.query(Article.published_timestamp).filter(Article.source_id == source_id).order_by(Article.published_timestamp.desc()).first()

def create_article(db: Session, article: schemas.ArticleBase):
    db_article = Article(origin_link=article.origin_link, source_id=article.source_id, title=article.title, body=article.body, tag=article.tag, published_timestamp=article.published_timestamp, thumbnail_image_link=article.thumbnail_image_link, created_at=article.created_at, author=article.author, body_image=article.body_image,description=article.description)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_all_articles(db: Session):
    db.query(Article).delete()
    db.commit()



    