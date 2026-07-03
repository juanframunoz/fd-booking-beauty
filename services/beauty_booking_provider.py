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


    def get_service_options(self, beauty_service):
        """Return service options prepared for website/API usage."""

        beauty_service.ensure_one()

        professionals = self.get_available_professionals(beauty_service)
        cabins = self.get_allowed_cabins(beauty_service)
        template = self.get_booking_template(beauty_service)

        return {
            "service_id": beauty_service.id,
            "service_name": beauty_service.name,
            "template_id": template.id if template else False,
            "template_name": template.name if template else False,
            "duration": beauty_service.duration,
            "price": beauty_service.list_price,
            "professionals": [
                {
                    "id": employee.id,
                    "name": employee.name,
                    "resource_id": employee.resource_id.id,
                    "duration": self.get_duration_for_employee(
                        beauty_service,
                        employee,
                    ),
                    "price": self.get_price_for_employee(
                        beauty_service,
                        employee,
                    ),
                }
                for employee in professionals
            ],
            "cabins": [
                {
                    "id": cabin.id,
                    "name": cabin.name,
                    "resource_id": cabin.booking_resource_id.id,
                    "cleaning_time": cabin.cleaning_time,
                }
                for cabin in cabins
            ],
        }
