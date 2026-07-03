# -*- coding: utf-8 -*-


class BeautyBookingFlowValidator:
    """Validation helper for Beauty booking flow."""

    def validate_service(self, service):
        if not service:
            return ["Service is required."]
        return []
