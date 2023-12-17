from pydantic import BaseModel as _BaseModel

class Blog(_BaseModel):
    title:str 
    body:str