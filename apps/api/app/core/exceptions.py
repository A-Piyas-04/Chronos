"""Application errors mapped to HTTP responses in ``main``."""

from __future__ import annotations


class ChronosError(Exception):
    """Base error with HTTP status and stable machine-readable ``code``."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        code: str = "error",
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class NotFoundError(ChronosError):
    def __init__(self, message: str = "Resource not found", *, code: str = "not_found") -> None:
        super().__init__(message, status_code=404, code=code)


class ConflictError(ChronosError):
    def __init__(self, message: str = "Conflict", *, code: str = "conflict") -> None:
        super().__init__(message, status_code=409, code=code)


class ValidationAppError(ChronosError):
    """Domain or cross-field validation failure (distinct from FastAPI body validation)."""

    def __init__(self, message: str, *, code: str = "validation_error") -> None:
        super().__init__(message, status_code=422, code=code)
