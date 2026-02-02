from pydantic import BaseModel, ConfigDict

class Chat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    
class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str