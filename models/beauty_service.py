# -*- coding: utf-8 -*-

from odoo import api, fields, models


class BeautyService(models.Model):
    _name = "fd.beauty.service"
    _description = "Beauty Service"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer(default=10)

    name = fields.Char(required=True, tracking=True)
    code = fields.Char()

    category_id = fields.Many2one(
        "fd.booking.category",
        string="Category",
    )

    booking_template_id = fields.Many2one(
        "fd.booking.template",
        string="Booking Template",
        required=True,
        ondelete="cascade",
    )

    duration = fields.Integer(
        string="Duration",
        default=30,
        help="Minutes",
    )

    preparation_time = fields.Integer(
        string="Preparation Time",
        default=0,
    )

    cleanup_time = fields.Integer(
        string="Cleanup Time",
        default=0,
    )

    list_price = fields.Float(
        string="Price",
    )

    allow_online = fields.Boolean(
        string="Allow Online Booking",
        default=True,
    )

    color = fields.Integer()

    image_1920 = fields.Image()

    description = fields.Html()

    employee_ids = fields.Many2many(
        "fd.booking.resource",
        string="Professionals",
    )

    product_ids = fields.Many2many(
        "product.product",
        string="Products",
    )

    employee_service_ids = fields.One2many(
        "fd.beauty.employee.service",
        "service_id",
        string="Professionals",
    )

    employee_count = fields.Integer(
        compute="_compute_employee_count",
    )

    booking_count = fields.Integer(
        compute="_compute_booking_count",
        string="Bookings",
    )

    @api.depends("booking_template_id")
    def _compute_booking_count(self):
        Booking = self.env["fd.booking"]

        for rec in self:
            if rec.booking_template_id:
                rec.booking_count = Booking.search_count([
                    ("booking_template_id", "=", rec.booking_template_id.id),
                ])
            else:
                rec.booking_count = 0
