"""Custom exceptions for the application."""


class TarpaulinException(Exception):
    """Base exception for Tarpaulin API."""
    pass


class BadRequestError(TarpaulinException):
    """Raised when request is invalid (400)."""
    pass


class UnauthorizedError(TarpaulinException):
    """Raised when authentication is required (401)."""
    pass


class ForbiddenError(TarpaulinException):
    """Raised when user lacks permission (403)."""
    pass


class NotFoundError(TarpaulinException):
    """Raised when resource is not found (404)."""
    pass


class ConflictError(TarpaulinException):
    """Raised when there's a conflict (409)."""
    pass