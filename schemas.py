from typing import List, Union
from pydantic import BaseModel

class ResponseBase(BaseModel):
  code: int = 200
  message: str = "Success"
  data: Union[object, None]  = None

class NewspaperSite(BaseModel):
    source_url: str
    source_rss: str
    
class ArticleBase(BaseModel):
    source_id: int # where is this data come from
    title: str  # title of the news
    body: str # body of the news including content
    tag: str # List but in str format, contains keywords of the news
    origin_link: str # link to the original news
    published_timestamp: int # publish time in timestamp
    thumbnail_image_link: str # link to the thumbnail image
    created_at: int # when this news is crawled
    author: str # author of the news
    description: str # description of the news
    body_image: str

    class Config:
        orm_mode = True
    
    
