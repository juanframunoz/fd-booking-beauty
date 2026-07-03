# -*- coding: utf-8 -*-


class BaseBookingFlowStep:
    """Base class for Beauty booking flow steps."""

    code = None

    def __init__(self, env):
        self.env = env

    def execute(self, context):
        return context


class SelectServiceStep(BaseBookingFlowStep):
    code = "select_service"

    def execute(self, context):
        service = context.get("service")
        if service:
            service.ensure_one()
        return context


class SelectProfessionalStep(BaseBookingFlowStep):
    code = "select_professional"

    def execute(self, context):
        return context


class SelectDateStep(BaseBookingFlowStep):
    code = "select_date"

    def execute(self, context):
        return context


class SelectTimeStep(BaseBookingFlowStep):
    code = "select_time"

    def execute(self, context):
        return context


class ConfirmBookingStep(BaseBookingFlowStep):
    code = "confirm_booking"

    def execute(self, context):
        return context
