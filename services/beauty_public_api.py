# -*- coding: utf-8 -*-

from odoo.addons.fd_booking_beauty.booking_flow.flow import BeautyBookingFlow


class BeautyPublicAPI:

    def __init__(self, env):
        self.env = env
        self.flow = BeautyBookingFlow(env)

    def get_service(self, service_id):

        result = self.flow.run({
            "service_id": service_id,
        })

        if not result.success:
            return {
                "success": False,
                "errors": result.errors,
            }

        data = result.data

        return {
            "success": True,
            "service": data["provider_data"],
            "recommended_professional":
                data["recommended_professional"].id
                if data.get("recommended_professional")
                else False,
        }


    def get_available_days(self, service_id, date_from, date_to):
        """Return available days for a beauty service.

        Contract prepared for the public website.
        """

        service = self.env["fd.beauty.service"].browse(service_id)

        if not service.exists():
            return {
                "success": False,
                "errors": ["Service not found."],
                "days": [],
            }

        calendar = self.flow.booking_service.get_calendar(
            booking_type=service.booking_template_id.booking_type_id,
            date_from=date_from,
            date_to=date_to,
            booking_template=service.booking_template_id,
        )

        return {
            "success": True,
            "service_id": service.id,
            "days": [
                {
                    "date": day["date"].isoformat(),
                    "available": day["available"],
                    "slot_count": day["slot_count"],
                }
                for day in calendar
            ],
        }

    def get_available_times(self, service_id, target_date, employee_id=False):
        """Return available times for a beauty service and date."""

        service = self.env["fd.beauty.service"].browse(service_id)

        if not service.exists():
            return {
                "success": False,
                "errors": ["Service not found."],
                "times": [],
            }

        resource = False

        if employee_id:
            employee = self.env["fd.beauty.employee"].browse(employee_id)
            resource = employee.resource_id if employee.exists() else False

        slots = self.flow.booking_service.get_slots(
            booking_type=service.booking_template_id.booking_type_id,
            target_date=target_date,
            booking_template=service.booking_template_id,
            resource=resource,
        )

        return {
            "success": True,
            "service_id": service.id,
            "date": target_date.isoformat(),
            "times": [
                {
                    "start": slot["start"].isoformat(),
                    "end": slot["end"].isoformat(),
                }
                for slot in slots
            ],
        }

    def create_booking(self, payload):
        """Create a beauty booking.

        Contract placeholder. Real booking creation will be implemented
        through BeautyBookingFlow and BookingService.
        """

        return {
            "success": False,
            "errors": ["Booking creation is not implemented yet."],
            "booking_id": False,
            "calendar_event_id": False,
            "portal_url": False,
        }
