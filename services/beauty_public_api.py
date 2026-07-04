# -*- coding: utf-8 -*-

from datetime import datetime

from odoo.addons.fd_booking.services.booking_service import BookingService
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

    def create_booking(
        self,
        service_id,
        start,
        end,
        customer,
        employee_id=False,
    ):
        service = self.env["fd.beauty.service"].sudo().browse(service_id)

        if not service.exists():
            return {
                "success": False,
                "errors": ["Service not found."],
                "booking_id": False,
            }

        customer = customer or {}

        partner = self.env["res.partner"].sudo().create({
            "name": customer.get("name") or "Beauty Customer",
            "email": customer.get("email") or False,
            "phone": customer.get("phone") or False,
        })

        resource = None

        if employee_id:
            employee = self.env["fd.beauty.employee"].sudo().browse(employee_id)
            if employee.exists():
                resource = employee.resource_id

        booking = BookingService(self.env).create_booking(
            booking_type=service.booking_template_id.booking_type_id,
            booking_template=service.booking_template_id,
            partner=partner,
            resource=resource,
            start_datetime=datetime.fromisoformat(start),
            end_datetime=datetime.fromisoformat(end),
            values={
                "name": service.name,
                "source": "website",
            },
        )

        return {
            "success": True,
            "errors": [],
            "booking_id": booking.id,
            "booking_name": booking.name,
            "partner_id": partner.id,
        }
