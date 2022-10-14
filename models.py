from pydantic import BaseModel


class Image(BaseModel):
    content: str
    filename: str
