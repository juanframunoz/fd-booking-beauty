# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import pytz

from odoo.addons.fd_booking.services.booking_service import BookingService
from odoo.addons.fd_booking_beauty.booking_flow.flow import BeautyBookingFlow


class BeautyPublicAPI:

    def __init__(self, env):
        self.env = env
        self.flow = BeautyBookingFlow(env)


    def _get_services_from_ids(self, service_ids):
        service_ids = service_ids or []
        services = self.env["fd.beauty.service"].sudo().browse(service_ids).exists()
        ordered = self.env["fd.beauty.service"]
        for service_id in service_ids:
            service = services.filtered(lambda item: item.id == service_id)
            if service:
                ordered |= service[:1]
        return ordered

    def get_services_summary(self, service_ids):
        services = self._get_services_from_ids(service_ids)

        if not services:
            return {
                "success": False,
                "errors": ["No services selected."],
                "summary": {},
            }

        templates = services.mapped("booking_template_id")
        summary = BookingService(self.env).calculate_template_summary(templates)

        return {
            "success": True,
            "errors": [],
            "service_ids": services.ids,
            "summary": summary,
        }

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

    def get_available_days(self, service_id, date_from, date_to, service_ids=None):
        selected_services = self._get_services_from_ids(service_ids) if service_ids else self.env["fd.beauty.service"]
        service = selected_services[:1] if selected_services else self.env["fd.beauty.service"].browse(service_id)

        if not service.exists():
            return {
                "success": False,
                "errors": ["Service not found."],
                "days": [],
            }

        templates = selected_services.mapped("booking_template_id") if selected_services else service.booking_template_id
        summary = BookingService(self.env).calculate_template_summary(templates)
        duration_minutes = summary.get("effective_duration") or service.booking_template_id.duration

        calendar = self.flow.booking_service.get_calendar(
            booking_type=service.booking_template_id.booking_type_id,
            date_from=date_from,
            date_to=date_to,
            booking_template=service.booking_template_id,
            duration_minutes=duration_minutes,
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

    def get_available_times(self, service_id, target_date, employee_id=False, service_ids=None):
        selected_services = self._get_services_from_ids(service_ids) if service_ids else self.env["fd.beauty.service"]
        service = selected_services[:1] if selected_services else self.env["fd.beauty.service"].browse(service_id)

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

        templates = selected_services.mapped("booking_template_id") if selected_services else service.booking_template_id
        summary = BookingService(self.env).calculate_template_summary(templates)
        duration_minutes = summary.get("effective_duration") or service.booking_template_id.duration

        slots = self.flow.booking_service.get_slots(
            booking_type=service.booking_template_id.booking_type_id,
            target_date=target_date,
            booking_template=service.booking_template_id,
            resource=resource,
            duration_minutes=duration_minutes,
        )

        booking_tz = pytz.timezone(service.booking_template_id.booking_type_id.timezone or "Europe/Madrid")

        return {
            "success": True,
            "service_id": service.id,
            "date": target_date.isoformat(),
            "times": [
                {
                    "start": pytz.UTC.localize(slot["start"]).astimezone(booking_tz).replace(tzinfo=None).isoformat(),
                    "end": pytz.UTC.localize(slot["end"]).astimezone(booking_tz).replace(tzinfo=None).isoformat(),
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
        service_ids=None,
    ):
        selected_services = self._get_services_from_ids(service_ids) if service_ids else self.env["fd.beauty.service"]
        service = selected_services[:1] if selected_services else self.env["fd.beauty.service"].sudo().browse(service_id)

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

        templates = selected_services.mapped("booking_template_id") if selected_services else service.booking_template_id
        summary = BookingService(self.env).calculate_template_summary(templates)

        booking_tz = pytz.timezone(service.booking_template_id.booking_type_id.timezone or "Europe/Madrid")
        local_start = booking_tz.localize(datetime.fromisoformat(start).replace(tzinfo=None))
        start_dt = local_start.astimezone(pytz.UTC).replace(tzinfo=None)
        end_dt = start_dt + timedelta(minutes=summary.get("effective_duration") or service.booking_template_id.duration)

        booking = BookingService(self.env).create_booking(
            booking_type=service.booking_template_id.booking_type_id,
            booking_template=service.booking_template_id,
            partner=partner,
            resource=resource,
            start_datetime=start_dt,
            end_datetime=end_dt,
            values={
                "name": " + ".join(selected_services.mapped("name")) if selected_services else service.name,
                "source": "website",
            },
        )

        service_by_template = {
            srv.booking_template_id.id: srv
            for srv in selected_services
            if srv.booking_template_id
        }

        for line in summary.get("lines", []):
            beauty_service = service_by_template.get(line["template_id"])

            self.env["fd.booking.line"].sudo().create({
                "booking_id": booking.id,
                "sequence": line["sequence"],
                "booking_template_id": line["template_id"],
                "name": beauty_service.name if beauty_service else line["name"],
                "original_duration": line["original_duration"],
                "price": beauty_service.list_price if beauty_service else line["price"],
            })

        return {
            "success": True,
            "errors": [],
            "booking_id": booking.id,
            "booking_name": booking.name,
            "partner_id": partner.id,
        }
