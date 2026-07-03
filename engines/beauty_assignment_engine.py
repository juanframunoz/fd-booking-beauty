# -*- coding: utf-8 -*-

from odoo.addons.fd_booking.services.booking_service import BookingService

from .assignment import (
    FirstAvailableStrategy,
    PriorityStrategy,
)


class BeautyAssignmentEngine:

    STRATEGIES = {
        "first_available": FirstAvailableStrategy,
        "priority": PriorityStrategy,
    }

    def __init__(self, env):
        self.env = env

    def select_professional(
        self,
        beauty_service,
        strategy="first_available",
    ):

        assignments = self.env["fd.beauty.employee.service"].search(
            [
                ("service_id", "=", beauty_service.id),
                ("active", "=", True),
                ("allow_online", "=", True),
                ("employee_id.active", "=", True),
            ],
            order="priority,sequence,id",
        )

        strategy_cls = self.STRATEGIES.get(
            strategy,
            FirstAvailableStrategy,
        )

        return strategy_cls(self.env).execute(assignments)


    def select_professional_for_slot(
        self,
        beauty_service,
        start_datetime,
        end_datetime,
        strategy="priority",
    ):
        beauty_service.ensure_one()

        booking_template = beauty_service.booking_template_id
        booking_type = booking_template.booking_type_id

        assignments = self.env["fd.beauty.employee.service"].search(
            [
                ("service_id", "=", beauty_service.id),
                ("active", "=", True),
                ("allow_online", "=", True),
                ("employee_id.active", "=", True),
            ],
            order="priority,sequence,id",
        )

        if not assignments:
            return self.env["fd.beauty.employee"]

        service = BookingService(self.env)
        available_resources = service.get_available_resources_for_slot(
            booking_type=booking_type,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            booking_template=booking_template,
        )

        available_assignments = assignments.filtered(
            lambda assignment: assignment.employee_id.resource_id in available_resources
        )

        if not available_assignments:
            return self.env["fd.beauty.employee"]

        strategy_cls = self.STRATEGIES.get(
            strategy,
            FirstAvailableStrategy,
        )

        return strategy_cls(self.env).execute(available_assignments)
