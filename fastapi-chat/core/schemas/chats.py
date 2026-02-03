from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class Chat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]


class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str = Field(
        min_length=1,
        max_length=50020,
    )
