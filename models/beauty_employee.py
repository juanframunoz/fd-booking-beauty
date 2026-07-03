# -*- coding: utf-8 -*-

from odoo import fields, models


class BeautyEmployee(models.Model):
    _name = "fd.beauty.employee"
    _description = "Beauty Professional"
    _order = "sequence, name"

    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    name = fields.Char(required=True)

    resource_id = fields.Many2one(
        "fd.booking.resource",
        required=True,
        ondelete="cascade",
        string="Booking Resource",
    )

    color = fields.Integer()

    image_1920 = fields.Image()

    employee_service_ids = fields.One2many(
        "fd.beauty.employee.service",
        "employee_id",
        string="Services",
    )

    service_count = fields.Integer(
        compute="_compute_service_count",
    )

    notes = fields.Html()
