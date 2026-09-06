from pydantic import BaseModel


class RestResponseDto(BaseModel):
    data: dict
    success: bool = True
    message: str = "OK"
