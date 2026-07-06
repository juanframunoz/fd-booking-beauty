# -*- coding: utf-8 -*-

from odoo import _

from odoo.addons.fd_booking.services.data_provider import DataProvider
from odoo.addons.fd_booking.services.data_provider_registry import DataProviderRegistry


class BeautyDataProvider(DataProvider):
    code = "beauty"
    name = _("Beauty")

    def templates(self, env):
        return [
            {
                "code": "services",
                "name": _("Beauty services"),
                "description": _("Import beauty services, durations and prices."),
                "formats": ["xlsx", "csv"],
            },
            {
                "code": "professionals",
                "name": _("Beauty professionals"),
                "description": _("Import beauty professionals."),
                "formats": ["xlsx", "csv"],
            },
            {
                "code": "cabins",
                "name": _("Beauty cabins"),
                "description": _("Import beauty cabins."),
                "formats": ["xlsx", "csv"],
            },
            {
                "code": "assignments",
                "name": _("Beauty assignments"),
                "description": _("Import professional-service assignments."),
                "formats": ["xlsx", "csv"],
            },
        ]


DataProviderRegistry.register(BeautyDataProvider())
