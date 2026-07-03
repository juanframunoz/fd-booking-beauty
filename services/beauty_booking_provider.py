# -*- coding: utf-8 -*-


class BeautyBookingProvider:
    """Beauty-specific booking rules.

    This provider translates Beauty concepts into FD Booking Engine concepts.
    """

    code = "beauty"

    def __init__(self, env):
        self.env = env

    def get_available_professionals(self, beauty_service):
        beauty_service.ensure_one()

        assignments = self.env["fd.beauty.employee.service"].search([
            ("service_id", "=", beauty_service.id),
            ("active", "=", True),
            ("allow_online", "=", True),
            ("employee_id.active", "=", True),
        ])

        return assignments.mapped("employee_id")

    def get_allowed_cabins(self, beauty_service):
        beauty_service.ensure_one()
        return beauty_service.cabin_ids.filtered(lambda c: c.active)

    def get_booking_template(self, beauty_service):
        beauty_service.ensure_one()
        return beauty_service.booking_template_id

    def get_duration_for_employee(self, beauty_service, beauty_employee):
        beauty_service.ensure_one()
        beauty_employee.ensure_one()

        assignment = self.env["fd.beauty.employee.service"].search([
            ("service_id", "=", beauty_service.id),
            ("employee_id", "=", beauty_employee.id),
            ("active", "=", True),
        ], limit=1)

        return assignment.duration if assignment else beauty_service.duration

    def get_price_for_employee(self, beauty_service, beauty_employee):
        beauty_service.ensure_one()
        beauty_employee.ensure_one()

        assignment = self.env["fd.beauty.employee.service"].search([
            ("service_id", "=", beauty_service.id),
            ("employee_id", "=", beauty_employee.id),
            ("active", "=", True),
        ], limit=1)

        return assignment.price if assignment and assignment.price else beauty_service.list_price
