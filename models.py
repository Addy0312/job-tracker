from typing import Optional
from pydantic import BaseModel

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    url: str
    source: str
    date_posted: Optional[str] = None
