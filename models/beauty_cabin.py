# -*- coding: utf-8 -*-

from odoo import fields, models


class BeautyCabin(models.Model):
    _name = "fd.beauty.cabin"
    _description = "Beauty Cabin"
    _order = "sequence, name"

    active = fields.Boolean(default=True)

    sequence = fields.Integer(default=10)

    name = fields.Char(
        required=True,
    )

    code = fields.Char()

    color = fields.Integer()

    image_1920 = fields.Image()

    capacity = fields.Integer(
        default=1,
    )

    cleaning_time = fields.Integer(
        string="Cleaning Time",
        default=0,
        help="Minutes after each booking.",
    )

    notes = fields.Html()

    booking_resource_id = fields.Many2one(
        "fd.booking.resource",
        required=True,
        ondelete="cascade",
        string="Booking Resource",
    )
