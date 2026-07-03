# -*- coding: utf-8 -*-

from odoo.addons.fd_booking_beauty.services.beauty_booking_provider import BeautyBookingProvider
from odoo.addons.fd_booking_beauty.booking_flow.steps import (
    SelectServiceStep,
    SelectProfessionalStep,
    SelectDateStep,
    SelectTimeStep,
    ConfirmBookingStep,
)
from odoo.addons.fd_booking_beauty.booking_flow.result import BookingFlowResult


class BeautyBookingFlow:
    """Booking flow orchestration for Beauty vertical."""

    def __init__(self, env):
        self.env = env
        self.provider = BeautyBookingProvider(env)
        self.steps = [
            SelectServiceStep(env),
            SelectProfessionalStep(env),
            SelectDateStep(env),
            SelectTimeStep(env),
            ConfirmBookingStep(env),
        ]

    def get_service_options(self, beauty_service):
        return self.provider.get_service_options(beauty_service)

    def get_recommended_professional(
        self,
        beauty_service,
        strategy="priority",
    ):
        return self.provider.get_recommended_professional(
            beauty_service,
            strategy=strategy,
        )

    def get_recommended_professional_for_slot(
        self,
        beauty_service,
        start_datetime,
        end_datetime,
        strategy="priority",
    ):
        from odoo.addons.fd_booking_beauty.engines.beauty_assignment_engine import BeautyAssignmentEngine

        return BeautyAssignmentEngine(self.env).select_professional_for_slot(
            beauty_service,
            start_datetime,
            end_datetime,
            strategy=strategy,
        )


    def run(self, context):
        """Run the Beauty booking flow."""

        context = context or {}

        for step in self.steps:
            context = step.execute(context)

        return BookingFlowResult(
            success=True,
            data=context,
        )
