from pydantic import BaseModel, ConfigDict

class Chat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str