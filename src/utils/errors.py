import logging
from fastapi import HTTPException, status
from typing import Dict, Any


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIError(HTTPException):
    """Custom API error class for consistent error responses"""
    
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


def create_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Create a standardized error response"""
    return {
        "detail": message
    }


# Common error responses
def unauthorized_error():
    return APIError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


def forbidden_error():
    return APIError(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


def not_found_error(item_type: str = "Item"):
    return APIError(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{item_type} not found"
    )


def already_exists_error(item_type: str = "Item"):
    return APIError(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{item_type} already exists"
    )


def validation_error(detail: str):
    return APIError(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail
    )


def unauthorized_access_error():
    return APIError(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to access this resource"
    )