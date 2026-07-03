# -*- coding: utf-8 -*-

from datetime import datetime, time, timedelta

from odoo import api, fields, models


class BeautyBookingWizard(models.TransientModel):
    _name = "fd.beauty.booking.wizard"
    _description = "Beauty Booking Wizard"

    service_id = fields.Many2one("fd.beauty.service", required=True)
    employee_id = fields.Many2one("fd.beauty.employee", string="Professional")
    booking_date = fields.Date(required=True)
    booking_time = fields.Float(string="Hour", required=True)
    partner_id = fields.Many2one("res.partner", string="Customer")

    duration = fields.Integer(compute="_compute_duration", readonly=True)
    price = fields.Float(compute="_compute_price", readonly=True)

    @api.depends("service_id", "employee_id")
    def _compute_duration(self):
        for rec in self:
            rec.duration = rec.service_id.duration or 0

    @api.depends("service_id", "employee_id")
    def _compute_price(self):
        for rec in self:
            rec.price = rec.service_id.list_price or 0

    def _get_start_datetime(self):
        self.ensure_one()
        hours = int(self.booking_time)
        minutes = int(round((self.booking_time - hours) * 60))
        return datetime.combine(
            self.booking_date,
            time(hour=hours, minute=minutes),
        )

    def _get_end_datetime(self):
        self.ensure_one()
        return self._get_start_datetime() + timedelta(minutes=self.duration)
