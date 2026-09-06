from functools import wraps
from typing import Callable

from flask import jsonify

from models import RestResponseDto


def rest_exception_handling_decorator(f: Callable):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Execute the actual endpoint logic
            data = f(*args, **kwargs)
            dto: RestResponseDto = RestResponseDto(data=data)
            return dto.model_dump(), 200
        except Exception as e:
            # Catch any exception and return a 500 error with the message
            dto: RestResponseDto = RestResponseDto(
                data=dict(),
                message=str(e),
                success=False,
            )
            return dto.model_dump(), 500
    return decorated_function
