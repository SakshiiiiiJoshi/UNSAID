from fastapi import HTTPException, status


class UnsaidBaseException(HTTPException):
    """Base exception for UNSAID API."""
    pass


class UserNotFound(UnsaidBaseException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


class InvalidCredentials(UnsaidBaseException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class MemoryNotFound(UnsaidBaseException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")


class SafetyEscalation(UnsaidBaseException):
    """Raised when the safety router detects urgent risk and the normal
    response pipeline should be bypassed."""
    def __init__(self, detail: str = "Safety escalation triggered"):
        super().__init__(status_code=status.HTTP_200_OK, detail=detail)
