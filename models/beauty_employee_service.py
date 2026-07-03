# -*- coding: utf-8 -*-

from odoo import fields, models


class BeautyEmployeeService(models.Model):
    _name = "fd.beauty.employee.service"
    _description = "Beauty Employee Service"
    _order = "sequence, employee_id, service_id"

    sequence = fields.Integer(default=10)

    active = fields.Boolean(default=True)

    employee_id = fields.Many2one(
        "fd.beauty.employee",
        required=True,
        ondelete="cascade",
    )

    service_id = fields.Many2one(
        "fd.beauty.service",
        required=True,
        ondelete="cascade",
    )

    duration = fields.Integer(
        string="Duration (min)",
        default=30,
    )

    price = fields.Float(
        string="Price",
    )

    priority = fields.Integer(
        default=10,
        help="Lower value = preferred professional.",
    )

    allow_online = fields.Boolean(
        default=True,
    )

    notes = fields.Text()
