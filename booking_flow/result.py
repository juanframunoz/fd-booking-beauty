# -*- coding: utf-8 -*-


class BookingFlowResult:
    """Simple result object for Beauty booking flows."""

    def __init__(self, success=True, data=None, errors=None):
        self.success = success
        self.data = data or {}
        self.errors = errors or []

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "errors": self.errors,
        }
