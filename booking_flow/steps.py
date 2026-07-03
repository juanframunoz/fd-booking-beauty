# -*- coding: utf-8 -*-


class BaseBookingFlowStep:
    """Base class for Beauty booking flow steps."""

    code = None

    def __init__(self, env):
        self.env = env

    def execute(self, state):
        return state


class SelectServiceStep(BaseBookingFlowStep):
    code = "select_service"

    def execute(self, state):
        service = state.context.get("service")
        if service:
            service.ensure_one()
        state.next("select_professional")
        return state


class SelectProfessionalStep(BaseBookingFlowStep):
    code = "select_professional"

    def execute(self, state):
        state.next("select_date")
        return state


class SelectDateStep(BaseBookingFlowStep):
    code = "select_date"

    def execute(self, state):
        state.next("select_time")
        return state


class SelectTimeStep(BaseBookingFlowStep):
    code = "select_time"

    def execute(self, state):
        flow = state.context.get("flow")

        if flow:
            booking_type = state.context.get("booking_type")
            booking_template = state.context.get("booking_template")

            if booking_type:
                resources = flow.booking_service.get_available_resources(
                    booking_type,
                    booking_template,
                )
                state.context["available_resources"] = resources

        state.next("confirm_booking")
        return state


class ConfirmBookingStep(BaseBookingFlowStep):
    code = "confirm_booking"

    def execute(self, state):
        state.finish()
        return state
